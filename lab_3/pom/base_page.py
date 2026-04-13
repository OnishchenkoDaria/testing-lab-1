from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from lab_3.utils.web_helpers import WebHelpers

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def open(self, url):
        self.driver.get(url)
        WebHelpers.wait_for_page_ready(self.driver)

    def wait_present(self, locator):
        return self.wait.until(expected_conditions.presence_of_element_located(locator))

    def wait_visible(self, locator):
        return self.wait.until(expected_conditions.visibility_of_element_located(locator))

    def wait_clickable(self, locator):
        return self.wait.until(expected_conditions.element_to_be_clickable(locator))

    def find(self, locator):
        return self.driver.find_element(*locator)

    def find_all(self, locator):
        return self.driver.find_elements(*locator)

    def scroll_to_element(self, element, block="center"):
        WebHelpers.scroll_into_view(self.driver, element, block)

    def js_click(self, element):
        WebHelpers.js_click(self.driver, element)