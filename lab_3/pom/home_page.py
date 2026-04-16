from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
import re

from lab_3.pom.base_page import BasePage
from lab_3.utils.web_helpers import WebHelpers
from selenium.webdriver.support import expected_conditions


class HomePage(BasePage):
    URL = "https://agro-yakist.com.ua/"

    RECOMMENDED_SECTION = (By.XPATH, "//*[contains(text(), 'Рекомендовані товари')]")
    MENU_MASK = (By.ID, "menuMask")
    MODAL_HEADING = (By.CSS_SELECTOR, ".modal-heading")
    MODAL_OVERLAY = (By.CSS_SELECTOR, ".mfp-container")
    MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, ".mfp-close")

    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".btn-addtocart")
    CART_BUTTON = (By.CSS_SELECTOR, "#cart > .btn")
    CART_REMOVE_BUTTONS = (By.CSS_SELECTOR, ".product-table-body-row .remove")
    CART_PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-table-body-row > .name")
    CART_PRODUCT_ROWS = (By.CSS_SELECTOR, "div.product-table-body-row")
    CART_QTY_PLUS = (By.CSS_SELECTOR, "div.quantity div.inner div:first-child")
    CART_QTY_MINUS = (By.CSS_SELECTOR, "div.quantity div.inner div:last-child")
    CART_QTY_INPUT = (By.CSS_SELECTOR, "div.quantity div.inner div:nth-child(2)")
    CART_ROW_PRICE = (By.CSS_SELECTOR, "div.product-table-body-row div.price")
    CART_ROW_TOTAL = (By.CSS_SELECTOR, "div.product-table-body-row div.total")
    CART_SUMMARY = (By.CSS_SELECTOR, "div.totals div#total-order")
    CART_PRODUCT_NAME = (By.CSS_SELECTOR, "div.name-left a")
    CART_STOCK_TEXT = (By.CSS_SELECTOR, "div.stock-text")
    CART_REMOVE_BTN = (By.CSS_SELECTOR, "div.remove input[type='button']")
    CART_EMPTY_MSG = (By.XPATH, "//*[contains(text(),'порожній') or contains(text(),'немає товарів')]")
    BTN_CONTINUE = (By.XPATH, "//*[contains(text(),'Продовжити покупки')]")
    BTN_CHECKOUT = (By.XPATH, "//*[contains(text(),'Оформлення замовлення')]")

    PROMO_TEXT = (By.CSS_SELECTOR, "p:nth-child(1)")
    LANGUAGE_DROPDOWN = (By.CSS_SELECTOR, ".lang")
    RUSSIAN_LANGUAGE_OPTION = (By.LINK_TEXT, "Русский")

    SEARCH_BAR = (By.ID, "inputs")
    SEARCH_RESULTS_HEADING = (By.CSS_SELECTOR, "h2")
    SEARCH_RESULTS_DESCRIPTION = (By.CSS_SELECTOR, "p:nth-child(4)")
    SEARCH_RESULTS_CONTENTS = (By.CSS_SELECTOR, ".product-layout:nth-child(1) > .product-thumb")
    PRODUCT_SPECIFICATION = (By.CSS_SELECTOR, ".specification tr:nth-child(4) > td:nth-child(2)")
    LOGIN_MENU = (By.CSS_SELECTOR, ".pull-right:nth-child(2) .hidden-sm")
    LOGIN_LINK = (By.LINK_TEXT, "Вхід")
    PASSWORD_FIELD = (By.ID, "input-password")
    EMAIL_FIELD = (By.ID, "input-email")
    LOGIN_SUBMIT_BTN = (By.LINK_TEXT, "Вхід")
    LOGIN_ERR_MSG = (By.CSS_SELECTOR, ".alert")

    def open_home_page(self):
        self.driver.get(self.URL)
        WebHelpers.wait_for_page_ready(self.driver)

    def scroll_to_recommended_section(self):
        recommended = self.wait_present(self.RECOMMENDED_SECTION)
        self.scroll_to_element(recommended, block="start")

    def close_menu_mask_if_present(self):
        WebHelpers.hide_overlay_if_present(
            self.driver,
            self.wait,
            self.MENU_MASK[0],
            self.MENU_MASK[1]
        )

    def type_in_search_bar(self, text: str):
        self.wait_visible(self.SEARCH_BAR).click()
        self.wait_visible(self.SEARCH_BAR).send_keys(text)
        self.wait_visible(self.SEARCH_BAR).send_keys(Keys.ENTER)

    def get_search_result_contents(self):
        return self.wait_visible(self.SEARCH_RESULTS_DESCRIPTION).text

    def get_search_results(self):
        return self.find_all(self.SEARCH_RESULTS_CONTENTS)

    def get_search_result_heading(self):
        return self.wait_visible(self.SEARCH_RESULTS_HEADING).text

    def navigate_to_item_by_name(self, name: str):
        self.driver.find_element(By.LINK_TEXT, name).click()
        return

    def  get_product_specification(self) -> str:
        return self.wait_visible(self.PRODUCT_SPECIFICATION).text

    def navigate_to_login_page(self):
        menu = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.LOGIN_MENU)
        )
        menu.click()

        login_link = WebDriverWait(self.driver, 10).until(
            expected_conditions.element_to_be_clickable(self.LOGIN_LINK)
        )
        login_link.click()

    def login_into_system(self):
        self.wait_visible(self.EMAIL_FIELD).send_keys("0507odv2005@gmail.com")
        self.wait_visible(self.PASSWORD_FIELD).send_keys("123456wrong")
        self.wait_clickable(self.LOGIN_SUBMIT_BTN).click()
        return

    def get_login_message(self):
        message = self.wait_visible(self.LOGIN_ERR_MSG).text
        return " ".join(message.split())

    def get_first_add_to_cart_button_element(self):
        self.scroll_to_recommended_section()
        self.close_menu_mask_if_present()
        first_button = self.wait_clickable(self.ADD_TO_CART_BUTTON)
        self.scroll_to_element(first_button, block="center")
        return first_button

    def click_first_add_to_cart_button(self):
        first_button = self.get_first_add_to_cart_button_element()
        self.js_click(first_button)

    def get_first_recommended_product_name(self):
        self.scroll_to_recommended_section()
        self.close_menu_mask_if_present()

        first_button = self.wait_clickable(self.ADD_TO_CART_BUTTON)

        # Try to find product name near the button
        try:
            product_name_element = first_button.find_element(
                By.XPATH,
                ".//preceding::a[normalize-space()][1]"
            )
            return product_name_element.text.strip()
        except:
            pass

        # fallback: search globally but pick first visible meaningful name
        elements = self.driver.find_elements(By.XPATH, "//a[normalize-space()]")

        for el in elements:
            text = el.text.strip()
            if len(text) > 5:  # filter junk like icons
                return text

        raise AssertionError("Could not determine product name")

    def add_first_recommended_product_to_cart(self):
        self.click_first_add_to_cart_button()

    def get_cart_modal_heading(self):
        return self.wait_visible(self.MODAL_HEADING).text

    def get_cart_products(self):
        self.wait_present(self.CART_PRODUCT_NAMES)
        return self.find_all(self.CART_PRODUCT_NAMES)

    def get_first_cart_product_name(self) -> str:
        product = self.get_cart_products()[0]
        return product.text.split("\n")[0].strip()

    def get_promo_text(self):
        return self.wait_visible(self.PROMO_TEXT).text

    def open_language_dropdown(self):
        dropdown = self.wait_clickable(self.LANGUAGE_DROPDOWN)
        dropdown.click()

    def is_russian_language_option_present(self):
        try:
            self.wait_visible(self.RUSSIAN_LANGUAGE_OPTION)
            return True
        except TimeoutException:
            return False

    def switch_language_to_russian(self):
        russian_option = self.wait_clickable(self.RUSSIAN_LANGUAGE_OPTION)
        russian_option.click()
        WebHelpers.wait_for_page_ready(self.driver)

    def close_cart_modal(self):
        try:
            close_btn = self.wait_clickable(self.MODAL_CLOSE_BUTTON)
            self.js_click(close_btn)
            self.wait.until(expected_conditions.invisibility_of_element_located(self.MODAL_OVERLAY))
        except TimeoutException:
            pass

    def open_cart(self):
        try:
            self.wait.until(expected_conditions.invisibility_of_element_located(self.MODAL_OVERLAY))
        except TimeoutException:
            pass

        cart_btn = self.wait_present(self.CART_BUTTON)
        self.scroll_to_element(cart_btn)
        self.js_click(cart_btn)

    def get_cart_remove_buttons(self):
        return self.find_all(self.CART_REMOVE_BUTTONS)

    def remove_first_product_from_cart(self):
        remove_buttons = self.get_cart_remove_buttons()
        if not remove_buttons:
            raise AssertionError("No remove button found in cart.")
        self.js_click(remove_buttons[0])

    def _wait_for_cart_update(self, timeout: int = 5) -> None:
        """Wait until the totals stop changing (cart AJAX is done)."""
        import time
        time.sleep(0.4)  # minimal settle; replace with staleness check
        WebDriverWait(self.driver, timeout).until(
            expected_conditions.presence_of_element_located(self.CART_SUMMARY)
        )

    def is_cart_empty(self) -> bool:
        try:
            WebDriverWait(self.driver, 4).until(
                lambda d: len(d.find_elements(*self.CART_PRODUCT_ROWS)) == 0
                or any(
                    e.is_displayed()
                    for e in d.find_elements(*self.CART_EMPTY_MSG)
                )
            )
        except Exception:
            pass  # fall through to explicit checks below

        rows = self.driver.find_elements(*self.CART_PRODUCT_ROWS)
        if rows:
            return False
        empty_els = self.driver.find_elements(*self.CART_EMPTY_MSG)
        return len(empty_els) > 0 and empty_els[0].is_displayed()

    def get_cart_product_quantity(self) -> int:
        el = WebDriverWait(self.driver, 5).until(
            expected_conditions.visibility_of_element_located(self.CART_QTY_INPUT)
        )
        return int((el.text or "1").strip())

    def increase_cart_quantity(self) -> None:
        btn = WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.CART_QTY_PLUS)
        )
        self.driver.execute_script("arguments[0].click();", btn)
        self._wait_for_cart_update()

    def decrease_cart_quantity(self) -> None:
        btn = WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.CART_QTY_MINUS)
        )
        self.driver.execute_script("arguments[0].click();", btn)
        self._wait_for_cart_update()

    def click_continue_shopping(self) -> None:
        btn = WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.BTN_CONTINUE)
        )
        self.driver.execute_script("arguments[0].click();", btn)

    def click_checkout(self) -> None:
        btn = WebDriverWait(self.driver, 5).until(
            expected_conditions.presence_of_element_located(self.BTN_CHECKOUT)
        )
        self.driver.execute_script("arguments[0].click();", btn)

    @staticmethod
    def _parse_price(text: str) -> float:
        text = text.replace(" ", "")  #remove space in thousands
        match = re.search(r"\d+[.,]?\d*", text)
        if match:
            return float(match.group().replace(",", "."))
        return 0.0

    def get_cart_row_price(self) -> float:
        el = self.driver.find_element(*self.CART_ROW_PRICE)
        return self._parse_price(el.text)

    def get_cart_row_total(self) -> float:
        el = self.driver.find_element(*self.CART_ROW_TOTAL)
        return self._parse_price(el.text)

    def get_cart_summary_total(self) -> float:
        el = self.driver.find_element(*self.CART_SUMMARY)
        return self._parse_price(el.text)