from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SearchPage(BasePage):
    _search_bar = By.CSS_SELECTOR, "[type='Search']"

    def search(self, search_str):
        """Searches for the provided search string."""
        self.find_element(self._search_bar).send_keys(search_str)

    def open_category(self, search_str):
        """Searches for the specified category and opens it."""
        def category_selector():
            return (By.XPATH,
                    f'//a[contains(@href, "/directory/category")]//p[text()="{search_str}"]')
        self.search(search_str)
        self.find_element(category_selector()).click()
