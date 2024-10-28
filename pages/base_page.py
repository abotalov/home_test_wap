from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions, ui


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = ui.WebDriverWait(driver, 5, poll_frequency=0.1)

    def find_element(self, locator):
        """Waits until the specified element is visible and returns it."""
        return self.wait.until(expected_conditions.visibility_of_element_located(locator))
    wait_for_element = find_element

    def find_element_non_obscured(self, locator):
        """Finds the first non-obscured element matching the locator."""
        def is_element_obscured():
            js_is_element_obscured = """
                var elem = arguments[0], box = elem.getBoundingClientRect(),
                    cx = box.left + box.width / 2, cy = box.top + box.height / 2,
                    e = document.elementFromPoint(cx, cy);
                for (; e; e = e.parentElement) {
                    if (e === elem)
                        return false;
                }
                return true;
            """
            return self.driver.execute_script(js_is_element_obscured, element)

        for element in self.find_elements(locator):
            if not is_element_obscured():
                return element
        return None

    def find_elements(self, locator):
        """Waits until all elements matching the locator are visible and returns them."""
        return self.wait.until(expected_conditions.visibility_of_all_elements_located(locator))
    wait_for_elements = find_elements

    def wait_until_element_absent(self, locator):
        """Waits until the specified element becomes absent."""
        self.wait.until_not(expected_conditions.presence_of_element_located(locator))

    def scroll_down_half_screen(self):
        """Scrolls down by half the viewport height and waits until scroll is performed."""
        def current_scroll_position():
            return self.driver.execute_script("return window.scrollY")

        initial_scroll_position = current_scroll_position()
        scroll_amount = self.driver.get_window_rect()["height"] // 2
        webdriver.ActionChains(self.driver).scroll_by_amount(0, scroll_amount).perform()
        expected_scroll_position = initial_scroll_position + scroll_amount
        try:
            self.wait.until(lambda _: current_scroll_position() == expected_scroll_position)
        except TimeoutException as exc:
            raise TimeoutException(
                f"Timeout waiting for scroll position to reach {expected_scroll_position}. "
                f"Current position at timeout is {current_scroll_position()}."
            ) from exc

    def wait_for_all_images_to_load(self):
        """Waits until all images on the page have loaded."""
        def all_images_loaded():
            js_are_images_loaded = """
                images = document.querySelectorAll("img");
                return Array.from(images).every((img) => img.complete && img.naturalWidth !== 0);
            """
            return self.driver.execute_script(js_are_images_loaded)

        self.wait.until(lambda _: all_images_loaded())

    def wait_for_video_to_load(self, element):
        """Waits for video element to be playable."""
        def is_video_loaded():
            js_is_video_loaded = "return arguments[0].readyState >= 2"
            return self.driver.execute_script(js_is_video_loaded, element)

        self.wait.until(lambda _: is_video_loaded())
