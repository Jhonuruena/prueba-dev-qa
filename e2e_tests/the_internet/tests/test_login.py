import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from e2e_tests.the_internet.utils.driver import get_driver
from e2e_tests.the_internet.pages.login_page import LoginPage
from e2e_tests.the_internet.data.test_data import TestData

class TestLogin:
    def setup_method(self):
        self.driver = get_driver()
        self.login_page = LoginPage(self.driver)

    def test_valid_login(self):
        self.login_page.open()
        self.login_page.login(TestData.USERNAME, TestData.PASSWORD)
        assert self.login_page.is_logged_in()

    def test_invalid_password(self):
        self.login_page.open()
        self.login_page.login(TestData.USERNAME, "wrongpass")

    def teardown_method(self):
        self.driver.quit()