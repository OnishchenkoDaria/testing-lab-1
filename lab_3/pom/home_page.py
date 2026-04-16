from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from lab_3.pom.base_page import BasePage
from lab_3.utils.web_helpers import WebHelpers
from selenium.webdriver.support import expected_conditions


class HomePage(BasePage):
    URL = "https://agro-yakist.com.ua/"

    RECOMMENDED_SECTION = (By.XPATH, "//*[contains(text(), 'Рекомендовані товари')]")
    MENU_MASK = (By.ID, "menuMask")
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, ".btn-addtocart")
    CART_BUTTON = (By.CSS_SELECTOR, "#cart > .btn")
    MODAL_HEADING = (By.CSS_SELECTOR, ".modal-heading")
    CART_REMOVE_BUTTONS = (By.CSS_SELECTOR, ".product-table-body-row .remove")
    CART_PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-table-body-row > .name")
    MODAL_OVERLAY = (By.CSS_SELECTOR, ".mfp-container")
    MODAL_CLOSE_BUTTON = (By.CSS_SELECTOR, ".mfp-close")

    PROMO_TEXT = (By.CSS_SELECTOR, "p:nth-child(1)")
    LANGUAGE_DROPDOWN = (By.CSS_SELECTOR, ".lang")
    RUSSIAN_LANGUAGE_OPTION = (By.LINK_TEXT, "Русский")

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