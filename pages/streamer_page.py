from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class StreamerPage(BasePage):
    _video = By.TAG_NAME, "video"

    def wait_for_page_to_load(self):
        """Waits until the streamer page has loaded."""
        video_element = self.find_element(self._video)
        self.wait_for_video_to_load(video_element)
