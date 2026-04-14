from selenium import webdriver
from lab_3.pom.home_page import HomePage

class TestAddingtocart:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def teardown_method(self, method):
        self.driver.quit()

    def test_addingtocart(self):
        home_page = HomePage(self.driver)

        home_page.open_home_page()
        home_page.add_first_recommended_product_to_cart()

        assert home_page.get_cart_modal_heading() == "Кошик"
        assert len(home_page.get_cart_products()) > 0