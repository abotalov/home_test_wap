import pathlib
from datetime import datetime


def save_screenshot(driver, file_name_part):
    """Saves screenshot of the current page with a timestamp."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    screenshot_dir = pathlib.Path("screenshots")
    screenshot_dir.mkdir(exist_ok=True)
    screenshot_path = str((screenshot_dir / f"{file_name_part}_{timestamp}.png").resolve())
    driver.save_screenshot(screenshot_path)
    return screenshot_path
