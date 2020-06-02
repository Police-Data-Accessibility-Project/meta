import pytest
from captcha.CaptchaSolver import CaptchaSolver
import os
import cv2


class TestCaptchaSolver:

    def test_folder_creation(self):
        # Note, this only removes the captcha folder in the tests directory.
        os.rmdir(os.path.join(os.getcwd(), 'captcha', 'incorrect'))
        os.rmdir(os.path.join(os.getcwd(), 'captcha', 'correct'))
        captcha_solver = CaptchaSolver(None)
        assert os.path.exists(os.path.join(os.getcwd(), 'captcha', 'incorrect'))
        assert os.path.exists(os.path.join(os.getcwd(), 'captcha', 'correct'))
        # Cleanup folders
        os.rmdir(os.path.join(os.getcwd(), 'captcha', 'incorrect'))
        os.rmdir(os.path.join(os.getcwd(), 'captcha', 'correct'))

    def test_ocr(self):
        # Do OCR on easy image to ensure it's working
        captcha_solver = CaptchaSolver(None)
        test_img1 = cv2.imread(os.path.join(os.getcwd(), 'test_ocr_valid.png'))
        test_img2 = cv2.imread(os.path.join(os.getcwd(), 'test_ocr_invalid.png'))
        captcha_text1 = captcha_solver.read_captcha(test_img1)
        captcha_text2 = captcha_solver.read_captcha(test_img2)
        assert captcha_text1 == '123'
        assert captcha_text2 == '12'

    def test_first_second_separation(self):
        # Tests correct separation of first_number (first 2 digits) and second_number (last digit)
        captcha_solver = CaptchaSolver(None)
        test_img = cv2.imread(os.path.join(os.getcwd(), 'test_ocr_valid.png'))
        assert captcha_solver.solve_captcha(test_img) == 15
        assert captcha_solver.first_number == 12
        assert captcha_solver.second_number == 3

    def test_first_second_separation_invalid(self):
        # Tests the case where only 2 out of 3 digits are read by OCR. Should return 0.
        captcha_solver = CaptchaSolver(None)
        test_img = cv2.imread(os.path.join(os.getcwd(), 'test_ocr_invalid.png'))
        assert captcha_solver.solve_captcha(test_img) == 0
        assert captcha_solver.first_number is None
        assert captcha_solver.second_number is None


    def test_captcha_fail_save(self):
        captcha_solver = CaptchaSolver(None)
        test_img = cv2.imread(os.path.join(os.getcwd(), 'test_ocr_valid.png'))
        captcha_solver.solve_captcha(test_img)
        captcha_solver.notify_last_captcha_fail()
        assert os.path.exists(os.path.join(os.getcwd(), 'captcha', 'incorrect', 'captcha1.png'))
        captcha_solver.notify_last_captcha_fail()
        assert os.path.exists(os.path.join(os.getcwd(), 'captcha', 'incorrect', 'captcha2.png'))

        os.remove(os.path.join(os.getcwd(), 'captcha', 'incorrect', 'captcha1.png'))
        os.remove(os.path.join(os.getcwd(), 'captcha', 'incorrect', 'captcha2.png'))

    def test_captcha_success_save(self):
        captcha_solver = CaptchaSolver(None)
        test_img = cv2.imread(os.path.join(os.getcwd(), 'test_ocr_valid.png'))
        captcha_solver.solve_captcha(test_img)
        captcha_solver.notify_last_captcha_success()
        assert os.path.exists(os.path.join(os.getcwd(), 'captcha', 'correct', '12+3=.png'))
        os.remove(os.path.join(os.getcwd(), 'captcha', 'correct', '12+3=.png'))
