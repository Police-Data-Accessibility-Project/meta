import pytest
from captcha.CaptchaSolver import CaptchaSolver
import os
import cv2

@pytest.fixture(scope='module')
def testdatadir(request):
    # Get a py.path.local, which is a bit friendlier to work with.
    return request.fspath.join('..')

class TestCaptchaSolver:

    def test_folder_creation(self, tmpdir):
        td = tmpdir.mkdir('captcha')
        captcha_solver = CaptchaSolver(None, outdir=td)

        assert os.path.exists(td.join('incorrect'))
        assert os.path.exists(td.join('correct'))

    def test_ocr(self, tmpdir, testdatadir):
        # Do OCR on easy image to ensure it's working
        td = tmpdir.mkdir('captcha')
        captcha_solver = CaptchaSolver(None, outdir=td)

        test_img1 = cv2.imread(testdatadir.join('test_ocr_valid.png').strpath)
        test_img2 = cv2.imread(testdatadir.join('test_ocr_invalid.png').strpath)
        captcha_text1 = captcha_solver.read_captcha(test_img1)
        captcha_text2 = captcha_solver.read_captcha(test_img2)

        assert captcha_text1 == '123'
        assert captcha_text2 == '12'

    def test_first_second_separation(self, tmpdir, testdatadir):
        # Tests correct separation of first_number (first 2 digits) and second_number (last digit)
        td = tmpdir.mkdir('captcha')
        captcha_solver = CaptchaSolver(None, outdir=td)

        test_img = cv2.imread(testdatadir.join('test_ocr_valid.png').strpath)

        assert captcha_solver.solve_captcha(test_img) == 15
        assert captcha_solver.first_number == 12
        assert captcha_solver.second_number == 3

    def test_first_second_separation_invalid(self, tmpdir, testdatadir):
        # Tests the case where only 2 out of 3 digits are read by OCR. Should return 0.
        td = tmpdir.mkdir('captcha')
        captcha_solver = CaptchaSolver(None, outdir=td)

        test_img = cv2.imread(testdatadir.join('test_ocr_invalid.png').strpath)

        assert captcha_solver.solve_captcha(test_img) == 0
        assert captcha_solver.first_number is None
        assert captcha_solver.second_number is None


    def test_captcha_fail_save(self, tmpdir, testdatadir):
        td = tmpdir.mkdir('captcha')
        captcha_solver = CaptchaSolver(None, outdir=td)
        test_img = cv2.imread(testdatadir.join('test_ocr_valid.png').strpath)

        captcha_solver.solve_captcha(test_img)
        captcha_solver.notify_last_captcha_fail()
        assert os.path.exists(td.join('incorrect', 'captcha1.png'))

        captcha_solver.notify_last_captcha_fail()
        assert os.path.exists(td.join('incorrect', 'captcha2.png'))

    def test_captcha_success_save(self, tmpdir, testdatadir):
        td = tmpdir.mkdir('captcha')
        captcha_solver = CaptchaSolver(None, outdir=td)
        test_img = cv2.imread(testdatadir.join('test_ocr_valid.png').strpath)

        captcha_solver.solve_captcha(test_img)
        captcha_solver.notify_last_captcha_success()

        assert os.path.exists(tmpdir.join('captcha', 'correct', '12+3=.png'))
