from selenium import webdriver
from selenium.webdriver.common.by import By
from lab_3.pom.home_page import HomePage


class TestERRsignin():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}
  
    def teardown_method(self, method):
        self.driver.quit()
  
    def test_eRRsignin(self):
        home_page = HomePage(self.driver)

        home_page.open_home_page()
        home_page.navigate_to_login_page()
        home_page.login_into_system("0507odv2005@gmail.com", "123456wrong")
        assert home_page.get_login_message() == "× E-Mail і/чи пароль не співпадають."

