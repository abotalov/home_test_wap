import pytest
import pytest_html
import undetected_chromedriver

from pages.category_page import CategoryPage
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.streamer_page import StreamerPage
from utilities import helpers


@pytest.fixture
def driver():
    """
    Initializes an undetected Chrome WebDriver with mobile device metrics.
    Undetected Chromedriver is used to bypass Twitch integrity check.
    """
    driver = undetected_chromedriver.Chrome()
    set_device_metrics_override = {
        "width": 412,
        "height": 915,
        "deviceScaleFactor": 3.5,  # Pixel ratio
        "mobile": True,
    }
    driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", set_device_metrics_override)
    driver.set_window_size(412, 915)
    yield driver
    driver.quit()


# This hook allows us to take screenshots on test failures
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield # Execute the test
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        test_name = item.nodeid.split('::')[-1]
        screenshot_path = helpers.save_screenshot(driver, test_name)
        extras = getattr(report, "extras", [])
        extras.append(pytest_html.extras.image(screenshot_path))
        report.extras = extras


@pytest.fixture
def base_url():
    """Returns the base URL."""
    return "https://m.twitch.tv/"


@pytest.fixture
def home_page(driver, base_url):
    """Initializes the HomePage object and navigates to the base URL."""
    driver.get(base_url)
    home_page_instance = HomePage(driver)
    home_page_instance.accept_cookies()
    return home_page_instance


@pytest.fixture
def category_page(driver):
    """Initializes the CategoryPage object."""
    return CategoryPage(driver)


@pytest.fixture
def search_page(driver):
    """Initializes the SearchPage object."""
    return SearchPage(driver)


@pytest.fixture
def streamer_page(driver):
    """Initializes the SearchPage object."""
    return StreamerPage(driver)
