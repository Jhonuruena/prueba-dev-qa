from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class UploadPage:
    def __init__(self, driver):
        self.driver = driver
        self.file_input = (By.ID, "file-upload")
        self.upload_button = (By.ID, "file-submit")
        self.uploaded_message = (By.TAG_NAME, "h3")
        self.uploaded_filename = (By.ID, "uploaded-files")

    def open(self):
        self.driver.get("https://the-internet.herokuapp.com/upload")

    def upload_file(self, file_path):
        file_input_element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(self.file_input)
        )
        file_input_element.send_keys(file_path)
        self.driver.find_element(*self.upload_button).click()

    def is_upload_successful(self):
        try:
            message = self.driver.find_element(*self.uploaded_message).text
            return "File Uploaded!" in message
        except:
            return False

    def get_uploaded_filename(self):
        return self.driver.find_element(*self.uploaded_filename).text
