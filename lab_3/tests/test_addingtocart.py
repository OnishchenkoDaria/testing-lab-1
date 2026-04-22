from selenium import webdriver
from lab_3.pom.home_page import HomePage

class TestAddingToCart:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def teardown_method(self, method):
        self.driver.quit()

    def test_add_product_to_cart(self):
        home_page = HomePage(self.driver)

        home_page.open_home_page()
        expected_product_name = home_page.get_first_recommended_product_name()
        home_page.add_first_recommended_product_to_cart()

        assert home_page.get_cart_modal_heading() == "Кошик"
        assert len(home_page.get_cart_products()) > 0
        assert home_page.get_first_cart_product_name() == expected_product_name