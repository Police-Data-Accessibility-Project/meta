import os
import sys
import csv
import re
import time
from typing import List
from pathvalidate import sanitize_filename
from dataclasses import dataclass


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


def save_download(directory, download_function, new_name, timeout=5):
    """
    Download a file and rename it. This is required as Selenium does not allow for the file download name to be specified.
    Based on this: https://stackoverflow.com/a/60900048/6008271
    :param directory: Download folder
    :param download_function: Function to start download (eg: link.click )
    :param new_name: Name to give downloaded file. Note: Do not include file extension as this is copied from the download.
    :param timeout: File download timeout
    :return: Path to downloaded file
    """
    files_start = os.listdir(directory)
    download_function()
    wait = True
    i = 0
    while (wait or len(os.listdir(directory)) == len(files_start)) and i < timeout * 2:
        time.sleep(0.5)
        wait = False
        for file_name in os.listdir(directory):
            if file_name.endswith('.part'):
                wait = True
    if i == timeout * 2:
        print("Timeout exceeded while downloading docket attachment.")
        return False
    else:
        try:
            downloaded_file = [name for name in os.listdir(directory) if name not in files_start][0]
            downloaded_file_path = os.path.join(directory, downloaded_file)
            extension = downloaded_file.split('.')[-1]
            new_file_path = parse_out_path(directory, new_name, extension)

            while not os.access(os.path.join(directory, downloaded_file), os.W_OK):
                time.sleep(0.5)
            try:
                os.rename(downloaded_file_path, new_file_path)
            except FileExistsError:
                # This record has been scraped before, so the attachment already exists.

                # If the new file is larger, it's possible the old one was corrupt.
                # In this case, delete the existing attachment and replace it.
                if os.path.getsize(downloaded_file_path) > os.path.getsize(new_file_path):
                    os.remove(new_file_path)
                    os.rename(downloaded_file_path, new_file_path)
                else:
                    print("Docket attachment already exists")
                    os.remove(os.path.join(directory, downloaded_file))
            return os.path.join(directory, downloaded_file)
        except IndexError:
            # If the download failed to start, this part will fail with an IndexError.
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
    total_len = len(os.path.join(directory, '{}.{}'.format(filename, extension)))
    if total_len > 256:
        # Shave excess characters from filename
        excess = total_len - 256
        filename = filename[:-excess]

    return os.path.join(directory, '{}.{}'.format(filename, extension))
