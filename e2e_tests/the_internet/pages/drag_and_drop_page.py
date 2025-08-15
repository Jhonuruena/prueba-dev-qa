from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

class DragAndDropPage:
    def __init__(self, driver):
        self.driver = driver
        self.column_a = (By.ID, "column-a")
        self.column_b = (By.ID, "column-b")

    def open(self):
        self.driver.get("https://the-internet.herokuapp.com/drag_and_drop")

    def drag_a_to_b(self):
        element_a = self.driver.find_element(*self.column_a)
        element_b = self.driver.find_element(*self.column_b)

        actions = ActionChains(self.driver)
        actions.drag_and_drop(element_a, element_b).perform()

    def get_header_a(self):
        return self.driver.find_element(*self.column_a).find_element(By.TAG_NAME, "header").text

    def get_header_b(self):
        return self.driver.find_element(*self.column_b).find_element(By.TAG_NAME, "header").text