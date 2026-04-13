from selenium import webdriver

def create_chrome_driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    return driver