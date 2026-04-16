from selenium import webdriver
from lab_3.pom.home_page import HomePage


class TestERRkeywordsearch():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_eRRkeywordsearch(self):
    home_page = HomePage(self.driver)

    home_page.open_home_page()
    home_page.type_in_search_bar("qwerty123nonexistent")

    assert home_page.get_search_result_contents() == "Немає продуктів які б відповідали критеріям пошуку."
    assert home_page.get_search_result_heading() == "Товари, які відповідають критеріям пошуку"
  
