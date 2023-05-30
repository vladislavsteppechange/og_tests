from utils.assertations import validate_data, validate_ex_default_state
from utils.screenshot_creater import make_screenshot
import re
from datetime import datetime
from playwright.sync_api import expect

# python3 -m pytest -s -v test_suit_OGEx.py --html-report=./Report/report.html

def test_layout_validation_OG_12(use_google_auth) -> None:
    """OG-12"""

    page = use_google_auth
    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass

    page.wait_for_timeout(1200)
    """validate sections"""
    expect(page.locator("//section[@class='strategy-selection']")).to_be_visible()
    expect(page.locator("//section[@class='occasion-selection']")).to_be_visible()
    expect(page.locator("//section[@class='relevant-occasions relevant-occasions--opened']")).to_be_visible()
    expect(page.locator("//section[@class='selected-occasion']")).to_be_visible()
    """validate 1-st section inputs"""
    input_params = page.locator("//section[@class='strategy-selection']//*[@class='select__title']").all()
    for item in input_params:
        expect(item).to_be_visible()
    expect(page.locator("//section[@class='strategy-selection']//*[@class='p-treeselect-label']")).to_be_visible()
    expect(page.locator("//section[@class='strategy-selection']//*[@class='time-range selector-group']//label")).to_be_visible()
    page.reload()


def test_appl_input_parameters_smoke_OG_13(use_google_auth) -> None:
    """OG - 13"""
    TCCC = 'TCCC'
    SPRITE = "Sprite"
    US = "United States"
    item = 'OG_13'
    screenshot = 'inputParams_sprite'
    current_date = datetime.now()
    start_day = int(current_date.day)
    stop_day = int(start_day) + 2
    page = use_google_auth
    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass

    """validate Adviser"""
    expect(page.locator("//section[@class='strategy-selection']//*[@class='p-dropdown p-component p-inputwrapper p-disabled p-inputwrapper-filled']")).to_be_visible()
    """validate default value"""
    assert page.locator("//section[@class='strategy-selection']//*[@class='p-dropdown p-component p-inputwrapper p-disabled p-inputwrapper-filled']").inner_text() == TCCC

    """validate Brand"""
    expect(page.locator("//section[@class='strategy-selection']//*[@class='product-select__input-wrapper']//*[text()='Brand']")).to_be_visible()
    """validate default value"""
    assert page.locator("//section[@class='strategy-selection']//*[@class='p-multiselect p-component p-inputwrapper p-multiselect-chip p-inputwrapper-filled']").inner_text() == SPRITE
    """click to brand selector"""
    page.locator("//section[@class='strategy-selection']//*[@class='p-multiselect p-component p-inputwrapper p-multiselect-chip p-inputwrapper-filled']//*[@class='p-multiselect-trigger']").click()
    page.get_by_role("option", name='Coca-cola').locator("div").nth(1).click()
    page.wait_for_timeout(500)

    """validate markets"""
    expect(page.locator("//section[@class='strategy-selection']//*[@class='p-treeselect-label']")).to_be_visible()
    """validate default value"""
    assert page.locator("//section[@class='strategy-selection']//*[@class='p-treeselect-label']").inner_text() == US
    """click to market selector"""
    page.locator("//section[@class='strategy-selection']//*[@class='p-treeselect-label']").click()
    page.get_by_role("button", name="Clear All").click()
    page.get_by_role("treeitem", name=US).locator("div").nth(2).click()
    page.locator("div").filter(has_text="SpainUnited KingdomUnited StatesClear AllApply").get_by_role("button",name="Apply").click()
    page.wait_for_timeout(500)

    """validate timeRange"""
    expect(page.locator("//*[@for='dateRange']")).to_be_visible()
    """validate input"""
    expect(page.locator("//input[@id='dateRange']")).to_be_visible()

    for item in range(1,3):
        """click to dateRange"""
        page.locator("//input[@id='dateRange']").click()
        page.wait_for_timeout(1200)

        if item == 1:
            """click clear to calendar"""
            page.locator("//*[@class='time-range__calendar-footer p-datepicker-buttonbar']//button[3]").click()
        else:
            """click to start date"""
            page.get_by_role("gridcell", name=str(start_day), exact=True).locator("span").click()
            """click next month"""
            page.locator("//*[@class='p-datepicker-header']//button[@class='p-datepicker-next p-link']").click()
            """click next date"""
            page.get_by_role("gridcell", name=str(stop_day), exact=True).locator("span").click()
            """click ok at calendar"""
            page.locator("//*[@class='time-range__calendar-footer p-datepicker-buttonbar']//button[1]").click()
            page.wait_for_timeout(1200)

    """validate Week Days"""
    expect(page.locator("//*[@class='time-range selector-group']//*[@class='select__container'][1]")).to_be_visible()
    page.wait_for_timeout(1200)
    """click to combo box"""
    page.locator("//*[@class='time-range selector-group']//*[@class='select__container'][1]").click()
    expect(page.locator("//*[@class='p-multiselect-header']")).to_contain_text("9 results are available")
    """validate combo box header"""
    expect(page.locator("//*[@class='p-multiselect-header']")).to_be_visible()
    """click to any week range"""
    page.locator("//li[@aria-label='Tuesday']").click()
    page.locator("//li[@aria-label='Thursday']").click()
    page.locator("//li[@aria-label='Friday']").click()
    page.wait_for_timeout(2200)

    """validate Day Parts"""
    expect(page.locator("//*[@class='time-range selector-group']//*[@class='select__container'][2]")).to_be_visible()
    page.wait_for_timeout(1200)
    """click to combo box"""
    page.locator("//*[@class='time-range selector-group']//*[@class='select__container'][2]").click()

    """click to some check box"""
    page.locator("//li[@aria-label='midday']").click()
    page.locator("//li[@aria-label='afternoon']").click()
    page.locator("//li[@aria-label='evening']").click()

    page.reload()
    page.wait_for_timeout(2200)
    """validate apply button for input params """
    expect(page.locator("//button[@class='p-button p-component primary-btn apply-btn']")).to_be_visible()
    page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()
    expect(page.locator("//*[@class='explore-occasion__footer-buttons strategy-selection__footer-buttons']//*[@class='p-button p-component p-disabled primary-btn apply-btn']")).to_be_visible()
    expect(page.locator("//*[@class='explore-occasion__footer-buttons strategy-selection__footer-buttons']//*[@class='p-button p-component p-disabled primary-btn apply-btn']")).to_be_disabled()

    """get screenshot"""
    page.wait_for_timeout(1000)
    make_screenshot(page, screenshot, item)
    selector = page.locator("//div[@class='media__container grid-container__item']")
    """get markets result that is a list"""
    validate_data(selector)

    """click to reset"""
    expect(page.locator("//*[@class='explore-occasion__footer-buttons strategy-selection__footer-buttons']//*[@class='p-button p-component secondary-btn reset-btn']")).to_be_visible()
    page.locator("//*[@class='explore-occasion__footer-buttons strategy-selection__footer-buttons']//*[@class='p-button p-component secondary-btn reset-btn']").click()

    """validate Adviser"""
    expect(page.locator("//section[@class='strategy-selection']//*[@class='p-dropdown p-component p-inputwrapper p-disabled p-inputwrapper-filled']")).to_be_visible()
    """validate default value"""
    assert page.locator("//section[@class='strategy-selection']//*[@class='p-dropdown p-component p-inputwrapper p-disabled p-inputwrapper-filled']").inner_text() == TCCC

    """validate Brand"""
    expect(page.locator("//section[@class='strategy-selection']//*[@class='product-select__input-wrapper']//*[text()='Brand']")).to_be_visible()
    """validate default value"""
    assert page.locator("//section[@class='strategy-selection']//*[@class='p-multiselect p-component p-inputwrapper p-multiselect-chip p-inputwrapper-filled']").inner_text() == SPRITE

    """validate sections"""
    sections = page.locator("//section").all()
    for item in sections:
        expect(item).to_be_visible()


def test_inputParams_brand_OG_37(use_google_auth)-> None:
    """goto app"""
    screenshot = 'inputParams_sprite'
    drop_down_items =[
        "Coca-cola","Diet Cola","Fanta","Sprite"
    ]
    page = use_google_auth
    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass
    for item in drop_down_items:
        page.locator("//section[@class='strategy-selection']//*[@class='p-multiselect p-component p-inputwrapper p-multiselect-chip p-inputwrapper-filled']").click()
        page.locator("div").filter(has_text=re.compile(r"^4 results are available$")).locator("div").nth(2).click()
        page.locator("div").filter(has_text=re.compile(r"^4 results are available$")).locator("div").nth(2).click()
        page.get_by_role("option", name=item).locator("div").nth(1).click()
        page.locator("section").filter(has_text="1. Input ParametersWhat you select here will impact an Occasion’s reach.Advertis") \
            .get_by_role("button", name="Apply").click()

        """get screenshot"""
        page.wait_for_timeout(1000)
        make_screenshot(page, screenshot, item)
        selector = page.locator("//div[@class='media__container grid-container__item']")

        """get markets result that is a list"""
        validate_data(selector)
    page.reload()


def test_inputParams_markets_OG_38(use_google_auth)-> None:
    """goto app"""
    screenshot = 'inputParams_markets'
    drop_down_items =[
        "United States","United Kingdom","Spain"
    ]
    page = use_google_auth
    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass

    for item in drop_down_items:
        page.locator("//section[@class='strategy-selection']//*[@class='p-treeselect-label']").click()
        page.get_by_role("button", name="Clear All").click()
        page.get_by_role("treeitem", name=item).locator("div").nth(2).click()
        page.locator("div").filter(has_text="SpainUnited KingdomUnited StatesClear AllApply").get_by_role("button",
                                                                                                          name="Apply").click()
        page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()

        """get screenshot"""
        make_screenshot(page, screenshot, item)
        selector = page.locator("//div[@class='media__container grid-container__item']")

        """get markets result that is a list"""
        validate_data(selector)
    page.reload()


def test_inputParams_date_choise_OG_39(use_google_auth)-> None:
    """goto app"""
    screenshot = 'inputParams_date'
    current_date = datetime.now()
    """set data value """
    start_day = int(current_date.day)
    stop_day = int(start_day) + 2

    item = f"{start_day}_{stop_day}"
    page = use_google_auth
    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass

    page.get_by_placeholder("Select Date Range").click()
    page.get_by_role("button", name="Previous Month").click()
    page.get_by_role("button", name="Previous Month").click()
    page.get_by_role("button", name="Previous Month").click()

    """days must be str type"""
    page.get_by_role("gridcell", name=str(start_day), exact=True).locator("span").click()
    page.get_by_text(str(stop_day)).click()

    page.get_by_role("button", name="OK").click()
    page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()

    """get screenshot"""
    make_screenshot(page, screenshot, item)
    selector = page.locator("//div[@class='media__container grid-container__item']")

    """get result that is a list"""
    page.wait_for_timeout(2000)
    validate_data(selector)
    page.reload()


def test_inputParams_week_days_OG_40(use_google_auth)-> None:
    """goto app"""
    screenshot = 'inputParams_week_days'
    drop_down_items =[
        "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday","Weekday","Weekend"
    ]
    page = use_google_auth
    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass


    for item in drop_down_items:
        page.locator(
            "div:nth-child(2) > .p-multiselect > .p-multiselect-label-container > .p-multiselect-label").click()
        page.locator("div").filter(has_text=re.compile(r"^9 results are available$")).locator("div").nth(2).click()
        page.locator("div").filter(has_text=re.compile(r"^9 results are available$")).locator("div").nth(2).click()
        page.get_by_text(item).click()
        page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()

        """get screenshot"""
        page.wait_for_timeout(1000)
        make_screenshot(page, screenshot, item)
        selector = page.locator("//div[@class='media__container grid-container__item']")

        """get markets result that is a list"""
        validate_data(selector)
    page.reload()


def test_inputParams_day_parts_OG_41(use_google_auth)-> None:
    """goto app"""
    screenshot = 'inputParams_day_parts'
    drop_down_items =["early morning","mid-morning","midday","afternoon","early evening","evening","night (after midnight)"
    ]
    page = use_google_auth
    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass


    for item in range(1,7):
        if item == 1:
            page.locator(
                "div:nth-child(3) > .p-multiselect > .p-multiselect-label-container > .p-multiselect-label").click()
            page.locator("div").filter(has_text=re.compile(r"^7 results are available$")).locator("svg").first.click()
            page.locator(f"//ul[@class='p-multiselect-items p-component']/li[1]").click()
            page.wait_for_timeout(2500)
            page.get_by_role("button", name="Close").click()
            page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()
        else:
            page.locator(
                "div:nth-child(3) > .p-multiselect > .p-multiselect-label-container > .p-multiselect-label").click()
            page.locator(f"//ul[@class='p-multiselect-items p-component']/li[{item}]").click()
            page.wait_for_timeout(2800)
            page.get_by_role("button", name="Close").click()
            page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()
        """get screenshot"""
        make_screenshot(page, screenshot, item)
        selector = page.locator("//div[@class='media__container grid-container__item']")

        """get markets result that is a list"""
        validate_data(selector)
    page.reload()


def test_filters_occ_type_OG_15(use_google_auth)-> None:
    """test Filters Occasion Type"""
    """goto app"""
    screenshot = 'occ_type'
    drop_down_items =["buy", "use"]
    page = use_google_auth
    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass
    page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()

    for item in drop_down_items:
        if item == 'buy':
            page.locator("//*[@class='select__title'][text()='Occasion Type']/following::div[@class='p-multiselect-label'][1]").click()
            page.locator("div").filter(has_text=re.compile(r"^2 results are available$")).locator("div").nth(2).click()

            page.get_by_role("option", name=item).locator("svg").click()
            page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()
            """get screenshot"""
            make_screenshot(page, screenshot, drop_down_items[0])
            selector = page.locator("//div[@class='media__container grid-container__item']")
            """get filterResult & assert that is a list"""
            validate_data(selector)
        else:
            page.locator("//*[@class='select__title'][text()='Occasion Type']/following::div[@class='p-multiselect-label'][1]").click()
            page.get_by_role("option", name=drop_down_items[0]).locator("svg").click()
            page.get_by_role("option", name=item).locator("svg").click()
            page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()
            """get screenshot"""
            make_screenshot(page, screenshot, drop_down_items[0])
            selector = page.locator("//div[@class='media__container grid-container__item']")
            """get filterResult & assert that is a list"""
            validate_data(selector)

    page.reload()


def test_filters_places_OG_34(use_google_auth)-> None:
    """test Filters Occasion Place"""
    """goto app"""
    screenshot = 'place'

    page = use_google_auth
    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass

    page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()
    for item in range(1,22):
        if item == 1:
            page.locator("div:nth-child(3) > .select__container > .p-multiselect > .p-multiselect-trigger").click()
            page.locator("div").filter(has_text=re.compile(r"^22 results are available$")).locator("svg").first.click()
            page.locator(f"//div[@class='p-multiselect-panel p-component p-ripple-disabled']//ul/li[{item}]").click()
            page.get_by_role("button", name="Close").click()
            page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()
            """get screenshot"""
            make_screenshot(page, screenshot, item)
            selector = page.locator("//div[@class='media__container grid-container__item']")
            """get filtersResult & assert that is a list"""
            validate_data(selector)
        else:
            page.locator("div:nth-child(3) > .select__container > .p-multiselect > .p-multiselect-trigger").click()
            page.locator(f"//div[@class='p-multiselect-panel p-component p-ripple-disabled']//ul/li[{item}]").click()
            page.get_by_role("button", name="Close").click()
            page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()
            """get screenshot"""
            make_screenshot(page, screenshot, item)
            selector = page.locator("//div[@class='media__container grid-container__item']")
            """get filtersResult & assert that is a list"""
            validate_data(selector)

    page.reload()


def test_filters_location_OG_35(use_google_auth)-> None:
    """test Filters Occasion Location"""
    """goto app"""
    screenshot = 'location'
    drop_down_items =[
        "at home","away from home"
    ]
    page = use_google_auth
    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass

    page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()

    """"filters option location"""
    for item in drop_down_items:
        if item == 'at home':
            page.locator("div:nth-child(5) > .select__container > .p-multiselect > .p-multiselect-trigger > .p-multiselect-trigger-icon").click()
            page.get_by_role("option", name=item).locator("div").nth(1).click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Close").click()
            page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()
        else:
            page.locator("div:nth-child(5) > .select__container > .p-multiselect > .p-multiselect-trigger > .p-multiselect-trigger-icon").click()
            page.get_by_role("option", name='at home').locator("div").nth(1).click()
            page.get_by_role("option", name=item).locator("div").nth(1).click()
            page.wait_for_timeout(1000)
            page.get_by_role("button", name="Close").click()
            page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()

        """get screenshot"""
        make_screenshot(page, screenshot, item)
        selector = page.locator("//div[@class='media__container grid-container__item']")

        """get searchResult & assert that is a list"""
        validate_data(selector)
    page.reload()


def test_filters_macro_occ(use_google_auth)-> None:
    """test Filters Occasion Macro"""
    """goto app"""
    screenshot = 'macro-occasions'
    drop_down_items =[
        "eating & drinking","household","leisure & culture",
        "physical activity","shopping"
    ]
    page = use_google_auth
    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass

    page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()

    """"filters option macro-Occasins"""
    for item in drop_down_items:
        page.locator("//section[@class='occasion-selection']//div[@class='p-treeselect-trigger']").click()
        page.get_by_role("button", name="Clear All").click()
        page.get_by_role("treeitem", name=item).locator("div").nth(2).click()
        page.locator("div").filter(has_text=re.compile(r"^Clear AllApply$")).get_by_role("button", name="Apply").click()
        page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()

        """get screenshot"""
        make_screenshot(page, screenshot, item)
        selector = page.locator("//div[@class='media__container grid-container__item']")

        """get searchResult & assert that is a list"""
        validate_data(selector)
    page.reload()


def test_filters_event(use_google_auth)-> None:
    """test Filters Occasion Event"""
    """goto app"""
    screenshot = 'event'
    drop_down_items =["any events","comedy","concert","festival",
                      "holidays","musical","show","sporting event","theatre","unidentified"
                      ]
    page = use_google_auth
    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass

    page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()

    """filters options"""
    for item in drop_down_items:
        if item == 'any events':
            page.locator("//section[@class='occasion-selection']//div[text()='Event']/following::*[@class='p-multiselect-trigger'][1]").click()
            page.locator("div").filter(has_text=re.compile(r"^10 results are available$")).locator("svg").first.click()
            page.get_by_role("option", name=item).locator("div").nth(1).click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Close").click()
            page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()
            """get screenshot"""
            make_screenshot(page, screenshot, item)
            selector = page.locator("//div[@class='media__container grid-container__item']")
            """get searchResult & assert that is a list"""
            validate_data(selector)
        else:
            page.locator(
                "//section[@class='occasion-selection']//div[text()='Event']/following::*[@class='p-multiselect-trigger'][1]").click()
            page.get_by_role("option", name=item).locator("div").nth(1).click()
            page.wait_for_timeout(2000)
            page.get_by_role("button", name="Close").click()
            page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()
            """get screenshot"""
            make_screenshot(page, screenshot, item)
            selector = page.locator("//div[@class='media__container grid-container__item']")
            """get searchResult & assert that is a list"""
            validate_data(selector)
    page.reload()


def test_filters_time(use_google_auth)-> None:
    """test Filters Occasion time"""
    """goto app"""
    screenshot = 'time'
    drop_down_items = [
        "breakfast","lunch","dinner","nighttime snack","midnight snack"
    ]
    page = use_google_auth

    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass

    page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()

    """"filters option time"""
    for item in drop_down_items:
        if item == 'breakfast':
            page.locator("div:nth-child(6) > .select__container > .p-multiselect > .p-multiselect-trigger > .p-multiselect-trigger-icon").click()
            page.locator("div").filter(has_text=re.compile(r"^5 results are available$")).locator("svg").first.click()
            page.get_by_role("option", name=item).locator("div").nth(1).click()
            page.get_by_role("button", name="Close").click()
            """get screenshot"""
            make_screenshot(page, screenshot, item)
            selector = page.locator("//div[@class='media__container grid-container__item']")
            """get searchResult & assert that is a list"""
            validate_data(selector)
        else:
            page.locator(
                "div:nth-child(6) > .select__container > .p-multiselect > .p-multiselect-trigger > .p-multiselect-trigger-icon").click()
            page.get_by_role("option", name=item).locator("div").nth(1).click()
            page.get_by_role("button", name="Close").click()
            """get screenshot"""
            make_screenshot(page, screenshot, item)
            selector = page.locator("//div[@class='media__container grid-container__item']")
            """get searchResult & assert that is a list"""
            validate_data(selector)
    page.reload()


def test_search(use_google_auth) -> None:
    """test Filters Occasion Serch Occasions"""
    screenshot = 'searchField'
    to_fill_occussion = ["art gallery", "coffee"]
    """go to app"""
    page = use_google_auth

    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass

    """activate search field"""
    for i in to_fill_occussion:
        page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()
        page.get_by_placeholder("Search Occasions").click()
        page.get_by_placeholder("Search Occasions").fill(i)
        page.get_by_role("option", name=i, exact=True).click()
        page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()

        """get screenshot"""
        make_screenshot(page, screenshot, i)
        selector = page.locator("//div[@class='media__container grid-container__item']")

        """get searchResult & assert that is a list"""
        validate_data(selector)
        page.reload()


def test_check_reset_and_apply_button_exp_occ_OG_42(use_google_auth) -> None:
    """test reset and apply ex occ"""
    """goto app"""
    screenshot = 'reset_and_apply'
    item = ['OG_42_1','OG_42_2']
    SPRITE = "Sprite"
    US = "United States"
    page = use_google_auth

    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass

    """click to brand get coca-cola"""
    page.locator(
        "//section[@class='strategy-selection']//*[@class='p-multiselect p-component p-inputwrapper p-multiselect-chip p-inputwrapper-filled']").click()
    page.get_by_role("option", name="Coca-Cola").locator("div").nth(1).click()
    """click close"""
    page.locator("//*[@class='p-multiselect-close p-link']").click()
    page.wait_for_timeout(400)

    """click to markets get Spain"""
    page.locator("//section[@class='strategy-selection']//*[@class='p-treeselect-label']").click()
    page.get_by_role("treeitem", name="Spain").locator("div").nth(2).click()
    page.locator("div").filter(has_text="SpainUnited KingdomUnited StatesClear AllApply").get_by_role("button",name="Apply").click()
    page.wait_for_timeout(400)

    """validate buttons and section"""
    expect(page.locator("//*[@class='explore-occasion__footer-buttons strategy-selection__footer-buttons']//button[1]")).to_be_enabled()
    expect(page.locator("//*[@class='explore-occasion__footer-buttons strategy-selection__footer-buttons']//button[2]")).to_be_enabled()
    expect(page.locator("//*[@class='select__title'][text()='Occasion Type']/following::div[@class='p-multiselect-label'][1]")).not_to_be_visible()
    expect(page.locator("//div[@class='media__container grid-container__item']")).not_to_be_visible()

    """click reset"""
    page.locator("//*[@class='explore-occasion__footer-buttons strategy-selection__footer-buttons']//button[1]").click()
    """validate buttons and section"""
    validate_ex_default_state(page, SPRITE, US)

    """screenshot"""
    make_screenshot(page, screenshot, item[0])
    """click to Apply"""
    page.locator("//button[@class='p-button p-component primary-btn apply-btn']").click()
    """validate Find Occ"""
    expect(page.locator("//section[@class='occasion-selection']//*[@class='select-group occasion-selection__filter-selectors']")).to_be_visible()

    """validate Occ section"""
    selector = page.locator("//div[@class='media__container grid-container__item']")
    validate_data(selector)
    """validate buttons and sections"""
    expect(page.locator("//*[@class='explore-occasion__footer-buttons strategy-selection__footer-buttons']//button[1]")).to_be_enabled()
    expect(page.locator("//*[@class='explore-occasion__footer-buttons strategy-selection__footer-buttons']//button[2]")).to_be_disabled()

    """click to reset"""
    page.locator("//*[@class='explore-occasion__footer-buttons strategy-selection__footer-buttons']//button[1]").click()
    validate_ex_default_state(page, SPRITE, US)
    page.wait_for_timeout(4000)
    page.reload()


def test_check_expand_and_collapse_button_ex_occ_OG_43(use_google_auth) -> None:
    """test Expand and Collapse at ex occ"""
    """goto app"""
    screenshot = 'expand_collapse'
    item = ['OG_43_1','OG_43_2']
    page = use_google_auth

    try:
        page.locator("//h3[text()='Explore Occasions']").click()
    except:
        pass
    """click to expand"""
    page.locator("//*[@class='collapse-toggle__aside collapse-toggle explore-occasion__left-toggle']").click()
    """validate Select Occasions"""
    expect(page.locator("//section[@class='relevant-occasions relevant-occasions--opened']")).to_be_visible()
    expect(page.locator("//section[@class='selected-occasion']")).to_be_visible()
    page.wait_for_timeout(700)
    make_screenshot(page, screenshot, item[0])
    """click to collapse"""
    page.locator("//*[@class='collapse-toggle__aside collapse-toggle explore-occasion__left-toggle']").click()
    """validate Apply button"""
    expect(page.locator("//*[@class='explore-occasion__footer-buttons strategy-selection__footer-buttons']//button[2]")).to_be_visible()
    page.wait_for_timeout(500)
    """clcik to Apply with default property"""
    page.locator("//*[@class='explore-occasion__footer-buttons strategy-selection__footer-buttons']//button[2]").click()
    page.wait_for_timeout(1500)
    """click to expand"""
    page.locator("//*[@class='collapse-toggle__aside collapse-toggle explore-occasion__left-toggle']").click()
    """validate sections"""
    expect(page.locator("//section[@class='relevant-occasions relevant-occasions--opened']")).to_be_visible()
    expect(page.locator("//section[@class='selected-occasion']")).to_be_visible()
    selector = page.locator("//div[@class='media__container grid-container__item']")

    """validate occasions get screenshot"""
    validate_data(selector)
    make_screenshot(page, screenshot, item[1])
    """click to collapse"""
    page.locator("//*[@class='collapse-toggle__aside collapse-toggle explore-occasion__left-toggle']").click()
    """validate Reset button"""
    expect(page.locator("//*[@class='explore-occasion__footer-buttons strategy-selection__footer-buttons']//button[1]")).to_be_visible()


