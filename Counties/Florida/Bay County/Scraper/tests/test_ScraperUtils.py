import pytest
from utils import ScraperUtils
import os


class TestScraperUtils:

    def test_parse_plea_case_numbers_blank(self):
        assert ScraperUtils.parse_plea_case_numbers("", [1, 2, 3]) == []

    def test_parse_plea_case_numbers__no_charge_mentioned(self):
        plea = "PLEA OF NOT GUILTY"
        assert ScraperUtils.parse_plea_case_numbers(plea, [1]) == []

    def test_parse_plea_case_numbers_one_charge_mentioned(self):
        plea = "DEFENDANT ENTERED PLEA OF : NOLO-CONTENDERE SEQ 2"
        assert ScraperUtils.parse_plea_case_numbers(plea, [1, 2]) == [2]

    def test_parse_plea_case_numbers_no_charge_numbers(self):
        plea = "DEFENDANT ENTERED PLEA OF NOLO CONTENDERE SEQ: 1,2,3,4,5"
        assert ScraperUtils.parse_plea_case_numbers(plea, []) == []

    def test_parse_plea_case_numbers_multiple_case_numbers(self):
        plea = "DEFENDANT ENTERED PLEA OF NOLO CONTENDERE SEQ: 1,2,3,4,5"
        assert ScraperUtils.parse_plea_case_numbers(plea, [1, 2, 3, 4, 5, 6]) == [1, 2, 3, 4, 5]

    def test_parse_plea_case_numbers_messy(self):
        # Test a really ugly plea docket I found in one case
        plea = "PLEA OF NOT GUILTY/DENIAL, WAIVER OF ARRAIGNMENT, DEMAND FOR NOTICE OF EXPERT TESTIMONY, DEMAND FOR DISCOVERY, DEMAND FOR STATEMENT OF PARTICULARS, DEMAND FOR JURY TRIAL, DESIGNATION OF E-MAIL ADDRESSES PURSUANT TO RULE 2.516 1/28/2020"
        assert ScraperUtils.parse_plea_case_numbers(plea, [1, 2, 3]) == []

    def test_parse_plea_type_blank(self):
        assert ScraperUtils.parse_plea_type('') is None

    def test_parse_plea_type_nolo_contendere(self):
        plea1 = 'PLEA OF NOLO CONTENDERE'
        plea2 = "DEFENDANT ENTERED PLEA OF : NOLO-CONTENDERE SEQ 2"
        plea3 = "DEFENDANT ENTERED PLEA OF NOLO CONTENDERE SEQ: 1,2,3,4,5"
        assert ScraperUtils.parse_plea_type(plea1) == 'Nolo Contendere'
        assert ScraperUtils.parse_plea_type(plea2) == 'Nolo Contendere'
        assert ScraperUtils.parse_plea_type(plea3) == 'Nolo Contendere'

    def test_parse_plea_type_guilty(self):
        plea1 = 'PLEA OF GUILTY'
        plea2 = 'DEFENDANT ENTERED PLEA OF : GUILTY SEQ 2'
        assert ScraperUtils.parse_plea_type(plea1) == 'Guilty'
        assert ScraperUtils.parse_plea_type(plea2) == 'Guilty'

    def test_parse_plea_type_not_guilty(self):
        plea1 = 'PLEA OF NOT GUILTY'
        plea2 = "PLEA OF NOT GUILTY/DENIAL, WAIVER OF ARRAIGNMENT, DEMAND FOR NOTICE OF EXPERT TESTIMONY, DEMAND FOR DISCOVERY, DEMAND FOR STATEMENT OF PARTICULARS, DEMAND FOR JURY TRIAL, DESIGNATION OF E-MAIL ADDRESSES PURSUANT TO RULE 2.516 1/28/2020"
        plea3 = 'EP - NOTICE OF APPEARANCE, AND ENTRY OF CONDITIONAL PLEA OF NOT GUILTY AND DEMAND FOR JURY TRIAL'
        assert ScraperUtils.parse_plea_type(plea1) == 'Not Guilty'
        assert ScraperUtils.parse_plea_type(plea2) == 'Not Guilty'
        assert ScraperUtils.parse_plea_type(plea3) == 'Not Guilty'

    def test_parse_defense_attorneys(self):
        attorneys1 = ['DEFENSE ATTORNEY: DOE, JANE EMILY ASSIGNED', 'DEFENSE ATTORNEY: DOE, JOHN MICHAEL ASSIGNED', 'DEFENSE ATTORNEY: SELF, SELF ASSIGNED']
        public_defenders1 = ['COURT APPOINTED ATTORNEY: DOE, JOHN MICHAEL ASSIGNED']
        assert ScraperUtils.parse_attorneys(attorneys1) == ['DOE, JANE EMILY', 'DOE, JOHN MICHAEL', 'SELF, SELF']
        assert ScraperUtils.parse_attorneys(public_defenders1) == ['DOE, JOHN MICHAEL']

    def test_parse_defense_attorneys_invalid(self):
        invalid_test = ['', '', '']
        invalid_test2 = []
        assert ScraperUtils.parse_attorneys(invalid_test) is None
        assert ScraperUtils.parse_attorneys(invalid_test2) is None

    def test_parse_out_path_illegal_characters(self):
        filename_invalid_chars = 't<>:e"/s\\t|?n*ame'
        assert ScraperUtils.parse_out_path('', filename_invalid_chars, 'pdf') == os.path.join('', 'testname.pdf')

    def test_parse_out_path_valid(self):
        # Function should not affect valid length filenames and paths.
        normal_filename = 'document'
        parsedPath = ScraperUtils.parse_out_path('C:\\Example\\Path', normal_filename, 'pdf')
        assert parsedPath == os.path.join('C:\\Example\\Path', '{}.{}'.format(normal_filename, 'pdf'))

    def test_parse_out_path_filename_extension_shortening(self):
        # 252 characters long, but with the .pdf extension it becomes 256 characters long - one too many.
        filename = '012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901'
        parsed_filename = ScraperUtils.parse_out_path('', filename, 'pdf')
        assert parsed_filename == '{}.{}'.format(filename[:-1], 'pdf')

    def test_parse_out_path_shortening(self):
        # 260 characters long before the extension. This is an invalid filename in Windows.
        filename_too_long = '01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789'
        parsed_path = ScraperUtils.parse_out_path(os.getcwd(), filename_too_long, 'txt')
        try:
            open(parsed_path, 'w')
            os.remove(parsed_path)
        except OSError:
            pytest.fail('parse_out_path() generates an invalid file path.')

    def test_parse_out_path_correct_length(self):
        # 260 characters long before the extension. This is an invalid filename in Windows.
        filename_too_long = '01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789'
        parsed_path = ScraperUtils.parse_out_path(os.getcwd(), filename_too_long, 'txt')
        assert len(parsed_path) <= 256
