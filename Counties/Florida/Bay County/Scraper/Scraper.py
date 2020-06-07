import sys
import getopt
import time
import os
import uuid
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException, TimeoutException

from captcha.CaptchaSolver import CaptchaSolver
import utils.ScraperUtils as ScraperUtils
from utils.ScraperUtils import Record, Charge

settings = {
    'portal-base': 'https://court.baycoclerk.com/BenchmarkWeb2/',
    'state-code': 'FL',
    'county': 'Bay',
    'start-year': 2000,
    'end-year': datetime.now().year,
    'missing-thresh': 5,
    'collect-pii': False,
    'connect-thresh': 10,
    'output': 'bay-county-scraped.csv',
    'save-attachments': 'none',
    'solve-captchas': False,
    'verbose': False
}

output_attachments = os.path.join(os.getcwd(), 'attachments')
output_file = os.path.join(os.getcwd(), settings['output'])

ffx_profile = webdriver.FirefoxOptions()
# Automatically dismiss unexpected alerts.
ffx_profile.set_capability('unexpectedAlertBehaviour', 'dismiss')
driver = webdriver.Firefox(options=ffx_profile)
captcha_solver = CaptchaSolver(driver)


def main():
    # Parse Arguments
    args = sys.argv[1:]
    short_args = 'p:s:c:y:e:t:pc:o:a:uv'
    long_args = ['portal-base=', 'state=', 'county', 'start-year=', 'end-year=', 'missing-thresh=', 'collect-pii',
                 'connect-thresh=', 'output=', 'save-attachments=','solve-captchas', 'verbose']

    try:
        args, vals = getopt.getopt(args, short_args, long_args)
        for arg, val in args:
            if arg in ('-p', '--portal-base'):
                settings['portal-base'] = val
            elif arg in ('-s', '--state'):
                settings['state-code'] = val
            elif arg in ('-c', '--county'):
                settings['county'] = val
            elif arg in ('-y', '--start-year'):
                settings['start-year'] = val
            elif arg in ('-e', '--end-year'):
                settings['end-year'] = val
            elif arg in ('-t', '--missing-thresh'):
                settings['missing-thresh'] = val
            elif arg in ('-p', '--collect-pii'):
                settings['collect-pii'] = True
            elif arg in ('-c', '--connect-thresh'):
                settings['connect-thresh'] = val
            elif arg in ('-o', '--output'):
                if val.endswith('.csv') or val.endswith('.CSV'):
                    settings['output'] = val
                else:
                    settings['output'] = '{}.csv'.format(val)
            elif arg in ('-a', '--save-attachments'):
                if val in {'none', 'filing', 'all'}:
                    settings['save-attachments'] = val
                else:
                    raise ValueError('Invalid value {} for argument --save-attachments (-a)'.format(val))
            elif arg in ('-u', '--solve-captchas'):
                settings['solve-captchas'] = True
            elif arg in ('-v', '--verbose'):
                settings['verbose'] = True
            else:
                raise ValueError('Invalid argument {} provided to Scraper.'.format(arg))
    except getopt.error as err:
        print("Unable to read arguments.", str(err))

    global output_file
    output_file = os.path.join(os.getcwd(), settings['output'])
    begin_scrape()


def begin_scrape():
    """
    Starts the scraping process. Continues from the last scraped record if the scraper was stopped before.
    :return:
    """
    global driver

    # Find the progress of any past scraping runs to continue from then
    try:
        last_case_number = ScraperUtils.get_last_csv_row(output_file).split(',')[3]
        print("Continuing from last scrape (Case number: {})".format(last_case_number))
        last_year = 2000 + int(str(last_case_number)[:2])  # I know there's faster ways of doing this. It only runs once ;)
        if not last_case_number.isnumeric():
            last_case_number = last_case_number[:-4]
        last_case = int(str(last_case_number)[-6:])
        settings['end-year'] = last_year
        continuing = True
    except FileNotFoundError:
        # No existing scraping CSV
        continuing = False
        pass

    # Scrape from the most recent year to the oldest.
    for year in range(settings['end-year'], settings['start-year'], -1):
        if continuing:
            N = last_case + 1
        else:
            N = 1

        print("Scraping year {} from case {}".format(year, N))
        YY = year % 100

        record_missing_count = 0
        # Increment case numbers until the threshold missing cases is met, then advance to the next year.
        while record_missing_count < settings['missing-thresh']:
            # Generate the case number to scrape
            case_number = f'{YY:02}' + f'{N:06}'

            search_result = search_portal(case_number)
            if search_result:
                record_missing_count = 0
                # if multiple associated cases are found,
                # scrape all of them
                if len(search_result) > 1:
                    for case in search_result:
                        search_portal(case)
                        scrape_record(case)
                # only a single case, no multiple associated cases found
                else:
                    scrape_record(case_number)
            else:
                record_missing_count += 1

            N += 1

        continuing = False

        print("Scraping for year {} is complete".format(year))


def scrape_record(case_number):
    """
    Scrapes a record once the case has been opened.
    :param case_number: The current case's case number.
    """
    # Wait for court summary to load
    for i in range(settings['connect-thresh']):
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'summaryAccordion')))
        except TimeoutException:
            if i == settings['connect-thresh'] - 1:
                raise RuntimeError('Summary details did not load for case {}.'.format(case_number))
            else:
                driver.refresh()

    # Get relevant page content
    summary_table_col1 = driver.find_elements_by_xpath('//*[@id="summaryAccordionCollapse"]/table/tbody/tr/td[1]/dl/dd')
    summary_table_col2 = driver.find_elements_by_xpath('//*[@id="summaryAccordionCollapse"]/table/tbody/tr/td[2]/dl/dd')
    summary_table_col3 = driver.find_elements_by_xpath('//*[@id="summaryAccordionCollapse"]/table/tbody/tr/td[3]/dl/dd')

    # Wait for court dockets to load
    for i in range(settings['connect-thresh']):
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'gridDocketsView')))
        except TimeoutException:
            if i == settings['connect-thresh'] - 1:
                raise RuntimeError('Dockets did not load for case {}.'.format(case_number))
            else:
                driver.refresh()

    charges_table = driver.find_elements_by_xpath('//*[@id="gridCharges"]/tbody/tr')
    docket_public_defender = driver.find_elements_by_xpath(
        "//*[contains(text(), 'COURT APPOINTED ATTORNEY') and contains(text(), 'ASSIGNED')]")
    docket_attorney = driver.find_elements_by_xpath("//*[contains(text(), 'DEFENSE') and contains(text(), 'ASSIGNED')]")
    docket_pleas = driver.find_elements_by_xpath("//*[contains(text(), 'PLEA OF')]")
    docket_attachments = driver.find_elements_by_class_name('casedocketimage')

    _id = str(uuid.uuid4())
    _state = settings['state-code']
    _county = settings['county']
    CaseNum = summary_table_col2[1].text.strip()
    AgencyReportNum = summary_table_col1[4].text.strip()
    ArrestDate = None  # Can't be found on this portal
    FilingDate = summary_table_col1[2].text.strip()
    OffenseDate = None  # Can't be found on this portal
    DivisionName = summary_table_col3[3].text.strip()
    CaseStatus = summary_table_col3[1].text.strip()

    if settings['collect-pii']:
        # Create list of assigned defense attorney(s)
        defense_attorney_text = list(map(lambda x: x.text, docket_attorney))
        DefenseAttorney = ScraperUtils.parse_attorneys(defense_attorney_text)
        # Create list of assigned public defenders / appointed attorneys
        public_defender_text = list(map(lambda x: x.text, docket_public_defender))
        PublicDefender = ScraperUtils.parse_attorneys(public_defender_text)
        # Get Judge
        Judge = summary_table_col1[0].text.strip()

        # Download docket attachments.
        # Todo(OscarVanL): This could be parallelized to speed up scraping if save-attachments is set to 'all'.
        if settings['save-attachments']:
            for attachment_link in docket_attachments:
                attachment_text = attachment_link.find_element_by_xpath('./../../td[3]').text.strip()
                if settings['save-attachments'] == 'filing':
                    if not ('CITATION FILED' in attachment_text or 'CASE FILED' in attachment_text):
                        # Attachment is not a filing, don't download it.
                        continue
                ScraperUtils.save_attached_pdf(driver, output_attachments, '{}-{}'.format(case_number, attachment_text),
                                               settings['portal-base'], attachment_link, 20, settings['verbose'])
    else:
        DefenseAttorney = []
        PublicDefender = []
        Judge = None

    Charges = {}
    for charge in charges_table:
        charge_details = charge.find_elements_by_tag_name('td')
        count = int(charge_details[0].text.strip())
        long_desc = charge_details[1].text.strip()
        # Statute is contained within brackets
        if '(' in long_desc and ')' in long_desc:
            statute = long_desc[long_desc.find('(') + 1:long_desc.find(')')]
        else:
            statute = None
        description = long_desc.split('(')[0]
        level = charge_details[2].text.strip()
        degree = charge_details[3].text.strip()
        # plea = charge_details[4].text.strip() # Plea is not filled out on this portal.
        disposition = charge_details[5].text.strip()
        disposition_date = charge_details[6].text.strip()
        offense_date = None  # Not shown on this portal
        citation_number = None  # Not shown on this portal
        Charges[count] = Charge(count, statute, description, level, degree, disposition, disposition_date, offense_date,
                                citation_number, None, None)

    # Pleas are not in the 'plea' field, but instead in the dockets.
    for plea_element in docket_pleas:
        plea_text = plea_element.text.strip()
        plea = ScraperUtils.parse_plea_type(plea_text)
        plea_date = plea_element.find_element_by_xpath('./../td[2]').text.strip()
        plea_number = ScraperUtils.parse_plea_case_numbers(plea_text, list(Charges.keys()))

        # If no case number is specified in the plea, then we assume it applies to all charges in the trial.
        if len(plea_number) == 0:
            for charge in Charges.values():
                charge.plea = plea
                charge.plea_date = plea_date
        else:
            # Apply plea to relevant charge count(s).
            for count in plea_number:
                Charges[count].plea = plea
                Charges[count].plea_date = plea_date

    ArrestingOfficer = None  # Can't be found on this portal
    ArrestingOfficerBadgeNumber = None  # Can't be found on this portal

    profile_link = driver.find_element_by_xpath("//table[@id='gridParties']/tbody/tr/*[contains(text(), 'DEFENDANT')]/../td[2]/div/a").get_attribute(
       'href')
    # profile_link = driver.find_element_by_xpath('//*[@id="gridParties"]/tbody/tr[1]/td[2]/div[1]/a').get_attribute(
    #     'href')
    load_page(profile_link, 'Party Details:', settings['verbose'])

    Suffix = None
    DOB = None  # This portal has DOB as N/A for every defendent
    Race = driver.find_element_by_xpath(
        '//*[@id="fd-table-2"]/tbody/tr[2]/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[7]/td[2]').text.strip()
    Sex = driver.find_element_by_xpath(
        '//*[@id="mainTableContent"]/tbody/tr/td/table/tbody/tr[2]/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[6]/td[2]').text.strip()
    FirstName = None
    MiddleName = None
    LastName = None
    PartyID = None

    # Only collect PII if configured
    if settings['collect-pii']:
        # Navigate to party profile
        full_name = driver.find_element_by_xpath(
            '//*[@id="mainTableContent"]/tbody/tr/td/table/tbody/tr[2]/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[1]/td[2]').text.strip()
        MiddleName = None
        LastName = None
        if ',' in full_name:
            name_split = full_name.split(',')[1].lstrip().split()
            FirstName = name_split[0]
            MiddleName = " ".join(name_split[1:])
            LastName = full_name.split(',')[0]
        else:
            # If there's no comma, it's a corporation name.
            FirstName = full_name
        PartyID = driver.find_element_by_xpath(
            '//*[@id="mainTableContent"]/tbody/tr/td/table/tbody/tr[2]/td[2]/table[2]/tbody/tr/td[2]/table/tbody/tr[8]/td[2]').text.strip()  # PartyID is a field within the portal system to uniquely identify defendants

    record = Record(_id, _state, _county, case_number, CaseNum, AgencyReportNum, PartyID, FirstName, MiddleName,
                    LastName, Suffix, DOB, Race, Sex, ArrestDate, FilingDate, OffenseDate, DivisionName, CaseStatus,
                    DefenseAttorney, PublicDefender, Judge, list(Charges.values()), ArrestingOfficer,
                    ArrestingOfficerBadgeNumber)
    ScraperUtils.write_csv(output_file, record, settings['verbose'])


def search_portal(case_number):
    """
    Performs a search of the portal from its home page, including selecting the case number input, solving the captcha
    and pressing Search. Also handles the captcha being solved incorrectly
    :param case_number: Case to search
    :return: A set of case number(s).
    """
    # Load portal search page
    load_page(f"{settings['portal-base']}/Home.aspx/Search", 'Search', settings['verbose'])
    # Give some time for the captcha to load, as it does not load instantly.
    time.sleep(0.8)

    # Select Case Number textbox and enter case number
    select_case_input()
    case_input = driver.find_element_by_id('caseNumber')
    case_input.click()
    case_input.send_keys(case_number)

    if settings['solve-captchas']:
        # Solve captcha if it is required
        try:
            # Get Captcha
            captcha_image_elem = driver.find_element_by_xpath(
                '//*/img[@alt="Captcha"]')
            captcha_buffer = captcha_image_elem.screenshot_as_png
            captcha_answer = captcha_solver.solve_captcha(captcha_buffer)
            captcha_textbox = driver.find_element_by_xpath(
                '//*/input[@name="captcha"]')
            captcha_textbox.click()
            captcha_textbox.send_keys(captcha_answer)
        except NoSuchElementException:
            # No captcha on the page, continue.
            pass

        # Do search
        search_button = driver.find_element_by_id('searchButton')
        search_button.click()
    else:
        raise Exception("Automated captcha solving is disabled by default. Please seek advice before using this feature.")

    # If the title stays as 'Search': Captcha solving failed
    # If the title contains the case number or 'Search Results': Captcha solving succeeded
    # If a timeout occurs, retry 'connect-thresh' times.
    for i in range(settings['connect-thresh']):
        try:
            # Wait for page to load
            WebDriverWait(driver, 5).until(
                lambda x: 'Search' in driver.title or case_number in driver.title or 'Search Results:' in driver.title)
            # Page loaded
            if driver.title == 'Search':
                # Clicking search did not change the page. This could be because of a failed captcha attempt.
                try:
                    # Check if 'Invalid Captcha' dialog is showing
                    driver.find_element_by_xpath(
                        '//div[@class="alert alert-error"]')
                    print("Captcha was solved incorrectly")
                    captcha_solver.notify_last_captcha_fail()
                except NoSuchElementException:
                    pass
                # Clear cookies so a new captcha is presented upon refresh
                driver.delete_all_cookies()
                # Try solving the captcha again.
                search_portal(case_number)
            elif 'Search Results: CaseNumber:' in driver.title:
                # Captcha solved correctly
                captcha_solver.notify_last_captcha_success()
                # Figure out the numer of cases returned
                case_detail_tbl = driver.find_element_by_tag_name('table').text.split('\n')
                case_count_idx = case_detail_tbl.index('CASES FOUND') + 1
                case_count = int(case_detail_tbl[case_count_idx])
                # Case number search found multiple cases.
                if case_count > 1:
                    return ScraperUtils.get_associated_cases(driver)
                # Case number search found no cases
                else:
                    return set()
            elif case_number in driver.title:
                # Captcha solved correctly
                captcha_solver.notify_last_captcha_success()
                # Case number search did find a single court case.
                return {case_number}
        except TimeoutException:
            if i == settings['connect-thresh'] - 1:
                raise RuntimeError('Case page could not be loaded after {} attempts, or unexpected page title: {}'.format(settings['connect-thresh'], driver.title))
            else:
                search_portal(case_number)


def select_case_input():
    """
    Selects the Case Number input on the Case Search window.
    """
    # Wait for case selector to load
    for i in range(settings['connect-thresh']):
        try:
            WebDriverWait(driver, 5).until(EC.text_to_be_present_in_element((By.ID, 'title'), 'Case Search'))
        except TimeoutException:
            if i == settings['connect-thresh'] - 1:
                raise RuntimeError('Portal homepage could not be loaded')
            else:
                load_page(f"{settings['portal-base']}/Home.aspx/Search", 'Search', settings['verbose'])

    case_selector = driver.find_element_by_xpath(
        '//*/input[@searchtype="CaseNumber"]')
    case_selector.click()
    try:
        case_input = driver.find_element_by_id('caseNumber')
        case_input.click()
    except ElementNotInteractableException:
        # Sometimes the caseNumber box does not appear, this is resolved by clicking to another radio button and back.
        name_selector = driver.find_element_by_xpath(
            '//*/input[@searchtype="Name"]')
        name_selector.cick()
        case_selector.click()
        case_input = driver.find_element_by_id('caseNumber')
        case_input.click()

    return case_input


def load_page(url, expectedTitle, verbose=False):
    """
    Loads a page, but tolerates intermittent connection failures up to 'connect-thresh' times.
    :param url: URL to load
    :param expectedTitle: Part of expected page title if page loads successfully. Either str or list[str].
    """
    if verbose:
        print('Loading page:', url)
    driver.get(url)
    for i in range(settings['connect-thresh']):
        try:
            if isinstance(expectedTitle, str):
                WebDriverWait(driver, 5).until(EC.title_contains(expectedTitle))
                return
            elif isinstance(expectedTitle, list):
                WebDriverWait(driver, 5).until(any(x in driver.title for x in expectedTitle))
                return
            else:
                raise ValueError('Unexpected type passed to load_page. Allowed types are str, list[str]')
        except TimeoutException:
            if i == settings['connect-thresh'] - 1:
                raise RuntimeError('Page {} could not be loaded after {} attempts. Check connction.'.format(url, settings['connect-thresh']))
            else:
                if verbose:
                    print('Retrying page (attempt {}/{}): {}'.format(i+1, settings['connect-thresh'], url))
                driver.get(url)

    print('Page {} could not be loaded after {} attempts. Check connection.'.format(url, settings['connect-thresh']),
          file=sys.stderr)


if __name__ == '__main__':
    if not os.path.exists(output_attachments):
        os.makedirs(output_attachments)
    main()
