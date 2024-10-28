from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class HomePage(BasePage):
    _accept_cookies_button = By.CSS_SELECTOR, "[data-a-target='consent-banner-accept']"
    _search_button = By.CSS_SELECTOR, "[aria-label='Search']"

    def accept_cookies(self):
        """
        Accepts the cookies consent by clicking the accept button and waits until it is absent.
        """
        self.find_element(self._accept_cookies_button).click()
        self.wait_until_element_absent(self._accept_cookies_button)

    def open_search(self):
        """Clicks on the search button to open the search interface."""
        self.find_element(self._search_button).click()
