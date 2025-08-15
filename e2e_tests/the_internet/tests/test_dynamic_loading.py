import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from e2e_tests.the_internet.utils.driver import get_driver
from e2e_tests.the_internet.pages.dynamic_loading_page import DynamicLoadingPage

class TestDynamicLoading:
    def setup_method(self):
        self.driver = get_driver()
        self.page = DynamicLoadingPage(self.driver)

    def test_wait_for_dynamic_content(self):
        self.page.open()
        self.page.click_start()
        self.page.wait_for_finish_text(timeout=10)
        assert self.page.get_finish_text() == "Hello World!"

    def teardown_method(self):
        self.driver.quit() 
