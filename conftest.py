import pytest
from playwright.sync_api import Playwright
import os
from dotenv import load_dotenv
load_dotenv()

EMAIL_USER = os.getenv('USER_MAIL')
EMAIL_PASS = os.getenv('MAIL_PASSWORD')
APP_URL = os.getenv('APP_URL_DEV')
USER_NAME = os.getenv('USER_NAME')
OMM_CAMPAIGN = "VL New Camapign 2023-05-19"




# APP_URL = 'https://c9h-og-frontend.pages.dev/#/'
# APP_URL_BETA = 'https://beta.c9h-og-frontend.pages.dev/#/'
# APP_URL_DEV = 'https://develop.c9h-og-frontend.pages.dev/#/'


@pytest.fixture(scope="session")
def use_ff_profile(playwright: Playwright)->None:
    user_path = 'home/vtest1/snap/firefox/common/.mozilla/firefox/8ay43uj2.default'
    context = playwright.firefox.launch_persistent_context(user_data_dir= user_path,
                                                           headless=False, slow_mo=500)
    page = context.new_page()
    page.set_viewport_size({"width": 1400, "height": 1400})
    page.goto(APP_URL)
    yield page
    context.close()



@pytest.fixture(scope='session')
def use_google_auth(playwright: Playwright)->None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(viewport={"width":1400,"height":1400},
                                  record_video_dir="./Report/videos",
                                  record_video_size={"width": 800, "height": 600})
    page = context.new_page()
    """basic navigate"""
    page.goto(APP_URL)

    page.wait_for_load_state()
    page.mouse.click(214, 845)

    with page.expect_popup() as page4:
      pass
    page.wait_for_load_state()
    page4 = page4.value
    page4.locator("//input[@type='email']").fill(EMAIL_USER)
    page4.get_by_role("button", name="Next").click()
    page4.get_by_role("textbox", name="Enter your password").click()
    page4.get_by_role("textbox", name="Enter your password").fill(EMAIL_PASS)
    page4.get_by_role("button", name="Next").click()
    page4.wait_for_timeout(2000)
    try:
        page4.locator("//input[@type='email']").fill(EMAIL_USER)
        page4.get_by_role("button", name="Next").click()
        page4.get_by_role("textbox", name="Enter your password").click()
        page4.get_by_role("textbox", name="Enter your password").fill(EMAIL_PASS)
        page4.get_by_role("button", name="Next").click()
        page4.wait_for_timeout(2000)
    except:
        pass
    page4.close()
    """navigate after login"""
    page.goto(APP_URL)
    page.mouse.click(214, 845)
    with page.expect_popup() as popup_page:
        pass
    popup_page = popup_page.value
    popup_page.locator("//*[@class='fFW7wc-ibnC6b-ssJRIf']", has_text=USER_NAME).click()
    page.wait_for_timeout(2000)
    popup_page.close()
    page.wait_for_timeout(2000)

    yield page
    context.close()
    browser.close()
