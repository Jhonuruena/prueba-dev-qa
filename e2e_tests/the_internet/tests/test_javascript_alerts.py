import sys
import os
import pytest
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from e2e_tests.the_internet.utils.driver import get_driver
from e2e_tests.the_internet.pages.alerts_page import AlertsPage

class TestJavaScriptAlerts:
    def setup_method(self):
        self.driver = get_driver()
        self.page = AlertsPage(self.driver)

    def test_js_alert(self):
        self.page.open()
        self.page.click_alert_button()

        alert_text = self.page.get_alert_text()
        assert alert_text == "I am a JS Alert"

        self.page.accept_alert()
        result = self.page.get_result_text()
        assert result == "You successfully clicked an alert"

    def test_js_confirm_accept(self):
        self.page.open()
        self.page.click_confirm_button()

        self.page.accept_alert()

        result = self.page.get_result_text()
        assert result == "You clicked: Ok"

    def test_js_confirm_dismiss(self):
        self.page.open()
        self.page.click_confirm_button()

        self.page.dismiss_alert()

        result = self.page.get_result_text()
        assert result == "You clicked: Cancel"

    def test_js_prompt_accept_with_text(self):
        self.page.open()
        self.page.click_prompt_button()

        self.page.send_keys_to_alert("haciendo prueba dev qa jhon")
        self.page.accept_alert()

        result = self.page.get_result_text()
        assert "haciendo prueba dev qa jhon" in result

    def test_js_prompt_dismiss(self):
        self.page.open()
        self.page.click_prompt_button()

        self.page.dismiss_alert()

        result = self.page.get_result_text()
        assert result == "You entered: null"

    def teardown_method(self):
        self.driver.quit()