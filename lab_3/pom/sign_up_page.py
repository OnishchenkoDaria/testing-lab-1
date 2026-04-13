from selenium.webdriver.common.by import By
from lab_3.pom.base_page import BasePage
from lab_3.utils.web_helpers import WebHelpers


class SignUpPage(BasePage):
    URL = "https://agro-yakist.com.ua/login/"

    def open_home_page(self):
        self.open(self.URL)