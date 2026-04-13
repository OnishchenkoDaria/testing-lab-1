from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class WebHelpers:
    @staticmethod
    def wait_for_page_ready(driver, timeout=10):
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

    @staticmethod
    def scroll_into_view(driver, element, block="center"):
        driver.execute_script(
            "arguments[0].scrollIntoView({block: arguments[1]});",
            element,
            block
        )

    @staticmethod
    def js_click(driver, element):
        driver.execute_script("arguments[0].click();", element)

    @staticmethod
    def hide_overlay_if_present(driver, wait, by, value):
        try:
            overlay = driver.find_element(by, value)
            if overlay.is_displayed():
                overlay.click()
                wait.until(EC.invisibility_of_element(overlay))
        except Exception:
            pass