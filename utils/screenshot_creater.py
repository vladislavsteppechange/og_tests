from pytest_html_reporter import attach
from playwright.sync_api import Page

def make_screenshot(page: Page, screenshot,item):
    page.wait_for_timeout(4000)
    attach(data=page.screenshot(path=f"./Report/screens/{screenshot}_{item}.png"))
