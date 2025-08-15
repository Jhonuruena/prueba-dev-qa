from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class DynamicLoadingPage:
    def __init__(self, driver):
        self.driver = driver
        self.start_button = (By.XPATH, "//button[text()='Start']")
        self.loading_indicator = (By.ID, "loading")
        self.finish_text = (By.ID, "finish")

    def open(self):
        self.driver.get("https://the-internet.herokuapp.com/dynamic_loading/2")

    def click_start(self):
        self.driver.find_element(*self.start_button).click()

    def wait_for_finish_text(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(self.finish_text)
        )

    def get_finish_text(self):
        return self.driver.find_element(*self.finish_text).text 
