import pytest
from selenium import webdriver
from lab_3.pom.home_page import HomePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

from lab_3.utils.web_helpers import WebHelpers


class TestCartManagement:
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(60)

    def teardown_method(self, method):
        self.driver.get(self.URL)
        WebHelpers.wait_for_page_ready(self.driver, timeout=20)

    def _add_one_product(self) -> HomePage:
        page = HomePage(self.driver)
        page.open_home_page()
        assert "agro-yakist.com.ua" in self.driver.current_url.lower()
        page.add_first_recommended_product_to_cart()
        assert page.get_cart_modal_heading() == "Кошик", "Cart modal did not open"
        assert len(page.get_cart_products()) > 0, "Cart is empty after add"
        return page

    #increase quantity → row total doubles
    def test_increase_quantity_updates_price(self):
        page = self._add_one_product()

        unit_price = page.get_cart_row_price()
        assert unit_price > 0, "Could not read unit price"

        # qty starts at 1 — increase to 2
        page.increase_cart_quantity()
        assert page.get_cart_product_quantity() == 2

        row_total   = page.get_cart_row_total()
        cart_total  = page.get_cart_summary_total()

        assert row_total  == pytest.approx(unit_price * 2, rel=0.01), \
            f"Row total {row_total} ≠ unit_price×2 ({unit_price * 2})"
        assert cart_total == pytest.approx(unit_price * 2, rel=0.01), \
            f"Cart summary {cart_total} ≠ unit_price×2 ({unit_price * 2})"
'''
    #decrease quantity
    def test_decrease_quantity_updates_price(self):
        page = self._add_one_product()

        unit_price = page.get_cart_row_price()

        page.increase_cart_quantity()
        page.decrease_cart_quantity()

        assert page.get_cart_product_quantity() == 1
        assert page.get_cart_row_total() == pytest.approx(unit_price, rel=0.01), \
            "Total did not return to unit price after decrement"

    #remove item
    def test_remove_product_empties_cart(self):
        page = self._add_one_product()

        page.remove_first_product_from_cart()

        assert page.is_cart_empty(), "Cart is not empty after removing the only product"

    #button "continue shopping" closes modal
    def test_continue_shopping_redirects_to_homepage(self):
        page = self._add_one_product()
        page.click_continue_shopping()

        WebDriverWait(self.driver, 6).until(
            expected_conditions.invisibility_of_element_located((By.CSS_SELECTOR, ".mfp-container"))
        )
        assert self.driver.current_url.rstrip("/") == HomePage.URL.rstrip("/"), \
            f"Expected homepage URL, got: {self.driver.current_url}"

    #button "Checkout" button navigates to order / checkout page
    def test_checkout_button_redirects_to_order_page(self):
        page = self._add_one_product()
        page.click_checkout()

        WebDriverWait(self.driver, 8).until(
            lambda d: d.current_url.rstrip("/") != HomePage.URL.rstrip("/")
        )
        current = self.driver.current_url
        assert any(kw in current for kw in ["checkout", "order", "cart", "zamovlennia"]), \
            f"Checkout URL does not look right: {current}"
'''