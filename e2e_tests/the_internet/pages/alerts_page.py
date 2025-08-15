from selenium.webdriver.common.by import By

class AlertsPage:
    def __init__(self, driver):
        self.driver = driver
        self.alert_button = (By.XPATH, "//button[text()='Click for JS Alert']")
        self.confirm_button = (By.XPATH, "//button[text()='Click for JS Confirm']")
        self.prompt_button = (By.XPATH, "//button[text()='Click for JS Prompt']")
        self.result_text = (By.ID, "result")

    def open(self):
        self.driver.get("https://the-internet.herokuapp.com/javascript_alerts")

    def click_alert_button(self):
        self.driver.find_element(*self.alert_button).click()

    def click_confirm_button(self):
        self.driver.find_element(*self.confirm_button).click()

    def click_prompt_button(self):
        self.driver.find_element(*self.prompt_button).click()

    def accept_alert(self):
        self.driver.switch_to.alert.accept()

    def dismiss_alert(self):
        self.driver.switch_to.alert.dismiss()

    def send_keys_to_alert(self, text):
        alert = self.driver.switch_to.alert
        alert.send_keys(text)

    def get_alert_text(self):
        return self.driver.switch_to.alert.text

    def get_result_text(self):
        return self.driver.find_element(*self.result_text).text