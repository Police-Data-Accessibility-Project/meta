import os
import numpy as np
import cv2
import pytesseract
import re


class CaptchaSolver:
    """Class for solving Captchas used on Benchmark-based Portals"""

    def __init__(self, driver, outdir=None):
        self.driver = driver
        self.outdir = outdir or os.path.join(os.getcwd(), 'captcha')
        self.correct_dir = os.path.join(self.outdir, 'correct')
        self.incorrect_dir = os.path.join(self.outdir, 'incorrect')
        self.current_captcha = None
        self.first_number = None
        self.second_number = None

        # Create necessary folders for saving correct/incorrect captchas
        os.makedirs(self.correct_dir, exist_ok=True)
        os.makedirs(self.incorrect_dir, exist_ok=True)

    def solve_captcha(self, captcha_buffer):
        """
        Solve Captcha and return its value
        :param captcha_buffer: Selenium screenshot buffer of captcha
        :return: Captcha answer
        """
        # Read digits in captcha
        captcha_digits = self.read_captcha(captcha_buffer)

        if len(captcha_digits) >= 3:
            # Do the sum
            self.first_number = int(captcha_digits[:2])
            self.second_number = int(captcha_digits[-1])
            captcha_sum = self.first_number + self.second_number
            return captcha_sum
        else:
            # Something went wrong during OCR.
            return 0

    def read_captcha(self, captcha_buffer):
        """
        Read the text contained in a captcha
        :param captcha_buffer: Selenium screenshot buffer of captcha
        :return: Text contained in captcha
        """
        self.current_captcha = self.__preprocess_captcha__(captcha_buffer)

        # Use Tesseract to perform OCR on processed captcha, using a limited character-set and Page Segmentation Mode 7
        captcha_text = pytesseract.pytesseract.image_to_string(self.current_captcha,
                                                               config="-c tessedit_char_whitelist=0123456789+=? --psm 7")
        # Remove any symbols from the text
        captcha_text = re.sub("[^0-9]", "", captcha_text)
        return captcha_text

    @staticmethod
    def __preprocess_captcha__(captcha_in):
        """
        Background noise can mostly be removed by thresholding HSV values. This is done in preprocessing.
        See https://stackoverflow.com/a/53978868/6008271
        :param captcha_in: Captcha to preprocess. Either as a Selenium screenshot buffer, or as a CV2 numpy ndarray.
        :return: Preprocessed captcha as opencv cv2 image
        """
        if isinstance(captcha_in, bytes):
            # Load from selenium screenshot_as_png into cv2 format
            captcha_nparr = np.frombuffer(captcha_in, np.uint8)
            captcha_img = cv2.imdecode(captcha_nparr, cv2.IMREAD_COLOR)
        elif isinstance(captcha_in, np.ndarray):
            # Already CV2 format
            captcha_img = captcha_in
        else:
            raise ValueError('Captcha image passed as invalid type:', type(captcha_in))

        # Convert captcha image to HSV colour space
        hsv = cv2.cvtColor(captcha_img, cv2.COLOR_BGR2HSV)

        # Mask the image's S and V values to suppress colour in the captcha
        mask = cv2.inRange(hsv, (0, 0, 0), (180, 45, 175))
        cv2.bitwise_and(captcha_img, captcha_img, mask=mask)
        # Invert the image to give white text on a black background
        captcha = cv2.bitwise_not(mask)

        return captcha

    def notify_last_captcha_fail(self):
        """
        If the last captcha was incorrectly solved, the Scraper should call this function to save the incorrect captcha
        """
        counter = 1
        filename = 'captcha{}.png'
        while os.path.isfile(os.path.join(self.incorrect_dir, filename.format(counter))):
            counter += 1

        cv2.imwrite(os.path.join(self.incorrect_dir, filename.format(counter)), self.current_captcha)

    def notify_last_captcha_success(self):
        """
        If the last captcha was correctly solved, the Scraper should call this function to save the correct captcha
        """
        cv2.imwrite(
            os.path.join(self.correct_dir, '{}+{}=.png'.format(self.first_number, self.second_number)),
            self.current_captcha)
