from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CategoryPage(BasePage):
    _streamer_xpath = By.XPATH, "//a[.//img[@class='tw-image']]"
    _follow_button = By.XPATH, "//div[text()='Follow']"

    def wait_for_page_to_load(self):
        """Waits until the category page has fully loaded."""
        self.wait_for_element(self._follow_button)
        self.wait_for_all_images_to_load()

    def open_visible_streamer(self):
        """Finds and clicks on the first non-obscured streamer link visible on the page."""
        self.find_element_non_obscured(self._streamer_xpath).click()
