from selenium import webdriver
from lab_3.pom.home_page import HomePage

class TestChaninglanguage:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def teardown_method(self, method):
        self.driver.quit()

    def test_chaninglanguage(self):
        home_page = HomePage(self.driver)

        home_page.open_home_page()

        assert home_page.get_promo_text() == (
            "Безкоштовна доставка «Новою поштою» та «Укрпоштою» до відділення "
            "при замовленні від 4000 грн за умови повної передплати "
            "(вага посилки — до 30 кг)"
        )

        home_page.open_language_dropdown()
        assert home_page.is_russian_language_option_present()

        home_page.switch_language_to_russian()

        assert home_page.get_promo_text() == (
            "Бесплатная доставка «Новой почтой» и «Укрпочтой» до отделения "
            "при заказе от 4000 грн при условии полной предоплаты "
            "(вес посылки — до 30 кг)"
        )