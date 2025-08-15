import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from e2e_tests.the_internet.utils.driver import get_driver
from e2e_tests.the_internet.pages.upload_page import UploadPage

class TestUpload:
    def setup_method(self):
        self.driver = get_driver()
        self.upload_page = UploadPage(self.driver)

    def test_file_upload(self):
        file_path = os.path.abspath("e2e_tests/the_internet/data/upload_test.txt")
        self.upload_page.open()
        self.upload_page.upload_file(file_path)

        assert self.upload_page.is_upload_successful()
        assert "upload_test.txt" in self.upload_page.get_uploaded_filename()

    def teardown_method(self):
        self.driver.quit() 
