from selenium.webdriver.common.by import By
from lab_3.pom.base_page import BasePage
from lab_3.utils.web_helpers import WebHelpers


class HomePage(BasePage):
    URL = "https://agro-yakist.com.ua/"

    RECOMMENDED_SECTION = (By.XPATH, "//*[contains(text(), 'Рекомендовані товари')]")
    MENU_MASK = (By.ID, "menuMask")
    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, ".btn-addtocart")
    MODAL_HEADING = (By.CSS_SELECTOR, ".modal-heading")
    CART_PRODUCT_NAMES = (By.CSS_SELECTOR, ".product-table-body-row > .name")

    def open_home_page(self):
        self.open(self.URL)

    def scroll_to_recommended_section(self):
        section = self.wait_present(self.RECOMMENDED_SECTION)
        self.scroll_to_element(section, block="start")

    def close_menu_mask_if_present(self):
        WebHelpers.hide_overlay_if_present(
            self.driver,
            self.wait,
            self.MENU_MASK[0],
            self.MENU_MASK[1]
        )

    def click_first_add_to_cart_button(self):
        button = self.wait_clickable(self.ADD_TO_CART_BUTTONS)
        self.scroll_to_element(button, block="center")
        self.js_click(button)

    def add_first_recommended_product_to_cart(self):
        self.scroll_to_recommended_section()
        self.close_menu_mask_if_present()
        self.click_first_add_to_cart_button()

    def get_cart_modal_heading(self):
        return self.wait_visible(self.MODAL_HEADING).text

    def get_cart_products(self):
        self.wait_present(self.CART_PRODUCT_NAMES)
        return self.find_all(self.CART_PRODUCT_NAMES)