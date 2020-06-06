import os
import sys
import csv
import re
from typing import List
from pathvalidate import sanitize_filename
from dataclasses import dataclass
import requests
from requests_toolbelt.utils import dump
from requests.exceptions import HTTPError, Timeout


@dataclass
class Charge:
    count: int
    statute: str
    description: str
    level: str
    degree: str
    disposition: str
    disposition_date: str
    offense_date: str
    citation_number: str
    plea: str
    plea_date: str


@dataclass
class Record:
    id: str
    state: str
    county: str
    portal_id: str
    case_num: str
    agency_report_num: str
    party_id: str
    first_name: str
    middle_name: str
    last_name: str
    suffix: str
    dob: str
    race: str
    sex: str
    arrest_date: str
    filing_date: str
    offense_date: str
    division_name: str
    case_status: str
    defense_attorney: str
    public_defender: str
    judge: str
    charges: List[Charge]
    arresting_officer: str
    arresting_officer_badge_number: str


def parse_plea_case_numbers(plea_text: str, valid_charges: List[int]) -> List[int]:
    """
    Attempts to find the charge count number (if any) a plea is referring to
    :param plea_text: Plea text in case dockets
    :param valid_charges: Valid charge numbers that can be referenced in the plea text
    :return: List of charge count numbers related to this plea
    """
    plea_text = plea_text.strip().split()
    if len(plea_text) > 0:
        plea_counts = re.sub('[^,0-9]', '', plea_text[-1]).split(',')
        plea_number = [int(charge) for charge in plea_counts if charge != '']
        # In rare cases numbers appear in the plea text not relating to a count number. Filter these out.
        filtered_plea_number = [charge for charge in plea_number if charge in valid_charges]
        return filtered_plea_number
    else:
        return []


def parse_attorneys(attorney_text: List[str]):
    """
    Gets a list of case docket strings and parses the attorney names from these
    :param attorney_text: List of case docket strings for the assignment of attorneys.
    :return: List of attorney names
    """
    attorneys = []
    for docket_text in attorney_text:
        attorney_name = docket_text.strip()
        if attorney_name.endswith('ASSIGNED'):
            # Remove ' ASSIGNED'
            attorney_name = attorney_name[:-9]
            # Remove text before attorney name
            attorney_name = attorney_name.split(':')[1].lstrip()
            attorneys.append(attorney_name)
        else:
            print("Docket begins with DEFENSE or COURT APPOINTED but does not end with ASSIGNED. Possible edge case?",
                  docket_text, file=sys.stderr)

    if len(attorneys) == 0:
        return None
    else:
        return attorneys


def parse_plea_type(plea_text: str):
    """
    Attempts to find the plea type
    :param plea_text: Plea text in case dockets
    :return: 'Not Guilty', 'Guilty', 'Nolo Contendere', or None.
    """
    if 'NOT' in plea_text:
        plea = 'Not Guilty'
    elif 'GUILTY' in plea_text:
        plea = 'Guilty'
    elif 'NOLO' in plea_text:
        # Nolo-Contendere (no contest) plea
        plea = 'Nolo Contendere'
    else:
        plea = None
    return plea


def write_csv(output_file, record: Record, verbose=False):
    """
    Writes a scraped case to the output CSV file
    :param output_file: Output path + filename of CSV
    :param record: Case record to write to CSV
    :param verbose: Print values being written
    """
    if verbose:
        print('-----------')
        print('_id', record.id)
        print('_state', record.state)
        print('_county', record.county)
        print('CaseNum', record.case_num)
        print('AgencyReportNumb', record.agency_report_num)
        print('PartyID', record.party_id)
        print('FirstName', record.first_name)
        print('MiddleName', record.middle_name)
        print('LastName', record.last_name)
        print('Suffix', record.suffix)
        print('DOB', record.dob)
        print('Race', record.race)
        print('Sex', record.sex)
        print('ArrestDate', record.arrest_date)
        print('FilingDate', record.filing_date)
        print('OffenseDate', record.offense_date)
        print('DivisionName', record.division_name)
        print('CaseStatus', record.case_status)
        print('DefenseAttorney', record.defense_attorney)
        print('PublicDefender', record.public_defender)
        print('Judge', record.judge)
        for charge in record.charges:
            print('ChargeCount', charge.count)
            print('ChargeStatute', charge.statute)
            print('ChargeDescription', charge.description)
            print('ChargeLevel', charge.level)
            print('ChargeDegree', charge.degree)
            print('ChargeDisposition', charge.disposition)
            print('ChargeDispositionDate', charge.disposition_date)
            print('ChargeOffenseDate', charge.offense_date)
            print('ChargeCitationNum', charge.citation_number)
            print('ChargePlea', charge.plea)
            print('ChargePleaDate', charge.plea_date)
        print('ArrestingOfficer', record.arresting_officer)
        print('ArrestingOfficerBadgeNumber', record.arresting_officer_badge_number)
        print('-----------')

    if os.path.isfile(output_file):
        # CSV exists, append to end of file
        with open(output_file, 'a', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            for charge in record.charges:
                writer.writerow(
                    [record.id, record.state, record.county, record.portal_id, record.case_num, record.agency_report_num, record.party_id,
                     record.first_name, record.middle_name, record.last_name, record.suffix, record.dob, record.race,
                     record.sex, record.arrest_date, record.filing_date, record.offense_date, record.division_name,
                     record.case_status, record.defense_attorney, record.public_defender, record.judge, charge.count,
                     charge.statute, charge.description, charge.level, charge.degree, charge.disposition,
                     charge.disposition_date, charge.offense_date, charge.citation_number, charge.plea,
                     charge.plea_date,
                     record.arresting_officer, record.arresting_officer_badge_number])
    else:
        # CSV does not exist. Write the headings
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(
                ['_id', '_state', '_county', 'PortalID', 'CaseNum', 'AgencyReportNum', 'PartyID', 'FirstName',
                 'MiddleName', 'LastName', 'Suffix', 'DOB', 'Race', 'Sex', 'ArrestDate', 'FilingDate', 'OffenseDate',
                 'DivisionName', 'CaseStatus', 'DefenseAttorney', 'PublicDefender', 'Judge', 'ChargeCount',
                 'ChargeStatute', 'ChargeDescription', 'ChargeLevel', 'ChargeDegree', 'ChargeDisposition',
                 'ChargeDispositionDate', 'ChargeOffenseDate', 'ChargeCitationNum', 'ChargePlea', 'ChargePleaDate',
                 'ArrestingOfficer', 'ArrestingOfficerBadgeNumber'])
            for charge in record.charges:
                writer.writerow(
                    [record.id, record.state, record.county, record.portal_id, record.case_num, record.agency_report_num, record.party_id,
                     record.first_name, record.middle_name, record.last_name, record.suffix, record.dob, record.race,
                     record.sex, record.arrest_date, record.filing_date, record.offense_date, record.division_name,
                     record.case_status, record.defense_attorney, record.public_defender, record.judge, charge.count,
                     charge.statute, charge.description, charge.level, charge.degree, charge.disposition,
                     charge.disposition_date, charge.offense_date, charge.citation_number, charge.plea,
                     charge.plea_date,
                     record.arresting_officer, record.arresting_officer_badge_number])


def get_last_csv_row(csv_file) -> str:
    """
    Gets last row of CSV file without having to load entire file into memory, as the parsed data CSV is expected to get large.
    :param csv_file: Path to CSV file
    :return: Last line of CSV file.
    """
    with open(csv_file, "r") as f:
        f.seek(0, 2)  # Seek @ EOF
        fsize = f.tell()  # Get Size
        f.seek(max(fsize - 1024, 0), 0)  # Set pos @ last n chars
        lines = f.readlines()  # Read to end

    line = lines[-1:][0]  # Get last line
    return line


def save_attached_pdf(driver, directory, name, portal_base, download_href, timeout=20, verbose=False):
    """
    Save a PDF docket attachment within a case.
    :param driver: Selenium driver
    :param directory: Directory to save attachment
    :param name: Name for PDF
    :param portal_base: Base URL for the portal. Eg: 'https://court.baycoclerk.com/BenchmarkWeb2/'
    :param download_href: Href for the download link, which holds attributes 'rel' (cid) and 'digest'.
    :param timeout: Time before aborting HTTP requests
    :param verbose: Print HTTP GET/POSTs for debugging
    :return: True (Success), False (Failure).
    """
    # Copy Selenium's user agent and headers to requests
    user_agent = driver.execute_script('return navigator.userAgent;')
    s = requests.Session()
    host = portal_base.split('/')[2]
    s.headers.update({'User-Agent': user_agent, 'Host': host, 'Connection': 'keep-alive', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br', 'Accept': 'text/css,*/*;q=0.1'})

    # It took me AGES to work this out, the portal does NOT handle cookies in a standard way. This meant my requests
    # always got 'access denied' even when I copied the cookies from Selenium to requests.
    portal_cookies = driver.get_cookies()
    cookie_header = ''
    for cookie in portal_cookies:
        cookie_header += '{}={}; '.format(cookie['name'], cookie['value'])
    cookie_header = cookie_header[:-2]  # Remove last deliminator '; '

    # Attempt to make the same HTTP requests as the website would, to be more stealthy ;)
    cid = download_href.get_attribute('rel')
    digest = download_href.get_attribute('digest')

    try:
        """
        This section does a GET request for PDFViewer2. 
        This stage may not be necessary, but I do it anyway so that later requests have a legitimate 'Referer' header.
        """
        if verbose:
            print('Sending GET: PDFViewer2')
        get_PDFViewer2_url = '{}Image.aspx/PDFViewer2?cid={}&digest={}'.format(portal_base, cid, digest)
        # GET for PDFViewer2 with cid and digest
        get_PDFViewer2 = requests.Request('GET', get_PDFViewer2_url, headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': driver.current_url,
            'Upgrade-Insecure-Requests': '1',
            'Cookie': cookie_header
        })
        prepared_get_PDFViewer2 = get_PDFViewer2.prepare()
        response = s.send(prepared_get_PDFViewer2, timeout=timeout)
        response.raise_for_status()  # Check HTTP status is 200 OK
        if verbose:
            print('Response for GET PDFViewer2 Received')
            data = dump.dump_all(response)
            print(data.decode('utf-8'))
            print('--------')
            print("Sending POST: getPDFRequestGuid")

        """
        This section does a POST for the attachment's access GUID
        """
        javascript_time = driver.execute_script('return String(new Date())').replace(' ', '+')
        # Get the Javascript time formatting, as this is embedded in the POST url.
        post_getPDFRequestGuid_url = '{}ImageAsync.aspx/GetPDFRequestGuid?cid={}&digest={}&time={}&redacted={}'.format(portal_base, cid, digest, javascript_time, False)
        post_getPDFRequestGuid = requests.Request('POST', post_getPDFRequestGuid_url, headers={
            'Accept': '*/*',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Origin': 'https://{}'.format(host),
            'Referer': get_PDFViewer2_url,
            'Cookie': cookie_header
        })

        prepared_post_getPDFRequestGuid = post_getPDFRequestGuid.prepare()
        response = s.send(prepared_post_getPDFRequestGuid, timeout=timeout)
        response.raise_for_status()  # Check HTTP status is 200 OK
        guid = response.content.decode('utf-8')
        if verbose:
            print("Response for POST getPDFRequestGuid received. GUID is:", guid)
            data = dump.dump_all(response)
            print(data.decode('utf-8'))
            print('--------')
            print("Sending GET: GetPDF")

        """
        This last section starts the download with a GET for the PDF itself.
        """
        get_GetPDF_url = '{}ImageAsync.aspx/GetPDF?guid={}'.format(portal_base, guid)
        get_GetPDF = requests.Request('GET', get_GetPDF_url, headers={
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer': get_PDFViewer2_url,
            'Upgrade-Insecure-Requests': str(1),
            'Cookie': cookie_header
        })

        prepared_get_GetPDF = get_GetPDF.prepare()
        response = s.send(prepared_get_GetPDF, timeout=timeout)
        response.raise_for_status()  # Check HTTP status is 200 OK
        if verbose:
            print("Response for GET GetPDF received.")

        outfile = parse_out_path(directory, name, 'pdf')
        with open(outfile, 'wb') as writer:
            try:
                writer.write(response.content)
            except OSError:
                print('Could not write attachment to file: {}'.format(outfile))
                return False
    except HTTPError as http_err:
        print('HTTP error occurred while downloading attachment {}: {}'.format(name, http_err))
        return False
    except Timeout:
        print('HTTP request/response timed out while downloading attachment {}'.format(name))
        return False


def parse_out_path(directory, filename, extension):
    """
    Ensures filenames given to downloaded docket attachments are valid. Strips disallowed characters and ensures path is not too long for Windows
    :param directory: Directory for file
    :param filename:  Name for file
    :param extension: Extension for file
    :return: Parsed out path.
    """
    # Sanitize name to avoid illegal characters.
    filename = sanitize_filename(filename)
    # 255 characters is the longest filename length in most filesystems
    filename_len = len('{}.{}'.format(filename, extension))
    if filename_len > 255:
        excess = filename_len - 255
        filename = filename[:-excess]
    # Shorten overall path to 256 chars.
    total_len = len(os.path.join(directory, '{}.{}'.format(filename, extension)))
    if total_len > 256:
        # Shave excess characters from filename
        excess = total_len - 256
        filename = filename[:-excess]

    return os.path.join(directory, '{}.{}'.format(filename, extension))


def get_associated_cases(driver):
    """
    When a  case number is associated with multiple cases, the search portal returns all those cases.
    This function returns all the associated case numbers.
    :param driver: Selenium driver
    :return: A set of case numbers
    """
    elems = driver.find_elements_by_class_name('sorting_1')
    case_nums = set([e.text for e in elems])
    return case_nums
