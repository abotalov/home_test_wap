from utilities import helpers


def test_select_streamer_and_save_screenshot(
        driver, home_page, search_page, category_page, streamer_page):
    """Select a streamer from the StarCraft II category and
    capture a screenshot of the streamer's page.
    """
    home_page.open_search()
    search_page.open_category("StarCraft II")
    category_page.wait_for_page_to_load()
    for _ in range(2):
        category_page.scroll_down_half_screen()
    category_page.open_visible_streamer()
    streamer_page.wait_for_page_to_load()
    helpers.save_screenshot(driver, "streamer")
