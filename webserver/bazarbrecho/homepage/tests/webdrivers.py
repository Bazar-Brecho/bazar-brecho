from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

HOMEPAGE_URL = "127.0.0.1:8000"


class ChromeWebdriver:
    def __init__(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def open_homepage(self):
        self.driver.get(HOMEPAGE_URL)

    def get_title(self):
        return self.driver.title

    def handle_web_element(self, xpath):
        try:
            element = self.driver.find_elements(By.XPATH, xpath)
            element[0].click()
        except IndexError:
            assert 0, "Element not found in page"
