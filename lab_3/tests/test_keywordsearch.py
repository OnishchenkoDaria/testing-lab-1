from selenium import webdriver
from selenium.webdriver.common.by import By
from lab_3.pom.home_page import HomePage


class TestKeywordsearch():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def test_keywordsearch(self):
        home_page = HomePage(self.driver)

        home_page.open_home_page()
        home_page.type_in_search_bar("кавун")

        elements = home_page.get_search_results()
        assert len(elements) > 0
        home_page.navigate_to_item_by_name("Кавун Чарльстон Грей / Charleston Gray 20 насінин (GSN-Semences)")
        assert home_page.get_product_specification() == "Кавуни"

