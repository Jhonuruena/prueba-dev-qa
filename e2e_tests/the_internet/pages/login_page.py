from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_input = (By.ID, "username")
        self.password_input = (By.ID, "password")
        self.login_button = (By.CSS_SELECTOR, "button[type='submit']")
        self.flash_message = (By.ID, "flash")
        self.logout_button = (By.LINK_TEXT, "Logout")

    def open(self):
        self.driver.get("https://the-internet.herokuapp.com/login")

    def login(self, username, password):
        self.driver.find_element(*self.username_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        self.driver.find_element(*self.login_button).click()

    def get_flash_message(self):
        return self.driver.find_element(*self.flash_message).text

    def is_logged_in(self):
        try:
            return self.driver.find_element(*self.logout_button).is_displayed()
        except:
            return False
