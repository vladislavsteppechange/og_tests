from utils.assertations import validate_data, validate_review_table, validate_priority,\
    validate_reach_reneview_table, validate_reach_reneview_table_for_few_sections,\
    validate_csv
from utils.screenshot_creater import make_screenshot
from utils.explore_company import explore_existing_company, explore_campaignfor_OG_18, \
    explore_occ_modal_inputs, explore_existing_campaign_OG_20, download_csv
from utils.right_bar_validate import validate_right_side_bar,\
    validate_start_interface, validate_updated_occ_after_confirm
from utils.unlink_occasions import unlink
from playwright.sync_api import expect
from datetime import datetime




# python3 -m pytest -s -v test_suit_OMM.py --html-report=./Report/report.html


def test_enter_own_Media_Manager_OG_16(use_google_auth) -> None:
    """OG - 16"""
    screenshot = 'manage_owned_media'
    item = 'enter_OMM'
    page = use_google_auth

    """Click on the link Manage Owned Media in the upper menu"""
    page.locator("//button[text()='Manage Owned Media']").click()

    """assert that is required interface"""
    page.wait_for_selector("//*[@class='own-media__header-title']")
    expect(page.locator("//*[@class='own-media__header-title']")).to_contain_text('Activate Occasion Strategy in Owned Media')

    """"Go back to the main page (click Occasion graph logo in the left upper corner)"""
    page.locator("//*[@class='header__logo']").click()

    """assert that is required interface"""
    page.wait_for_selector("//*[@class='home__greeting']")
    expect(page.locator("//*[@class='home__greeting']")).to_be_visible()

    """Click on the button Manage Owned Media on the main screen Expected result"""
    page.locator("//nav/a[3]").click()

    """assert that is required interface"""
    page.wait_for_selector("//*[@class='own-media__header-title']")
    expect(page.locator("//*[@class='own-media__header-title']")).to_contain_text('Activate Occasion Strategy in Owned Media')


def test_check_for_the_advertiser_brands_dropdown_OG_17(use_google_auth) -> None:
    """OG - 17"""
    screenshot = 'manage_owned_media'
    item = 'brand_dropdown'
    drop_down_items = [
        "Sprite","Fanta","Diet Cola", "Coca-Cola"
    ]
    page = use_google_auth
    page.reload()
    page.wait_for_timeout(1000)
    # page.locator("//header//button[3]").click()
    # page.wait_for_timeout(1000)

    """Advertiser dropdown has one value TCCC by default"""
    assert page.locator("//span[@aria-label='TCCC']").inner_text() == 'TCCC'

    """assert inputs are disabled, when brands is not exist"""
    expect(page.locator("//*[@class='p-dropdown-label p-inputtext'][text()='Select Existing Campaign']")).not_to_be_visible()
    page.reload()

    page.locator("//*[@class='p-multiselect-label']").click()
    page.wait_for_timeout(1000)
    page.locator("//div[@class='p-multiselect-panel p-component p-ripple-disabled']//div/div[@class='p-checkbox p-component']").click()
    page.wait_for_timeout(1000)
    page.locator("//*[@class='p-checkbox-box p-highlight p-focus']").click()

    """choose brands from combobox"""
    for i in range(4):
        page.locator(f"//ul/li[{i+1}]//*[@class='p-checkbox-box']").click()
        page.wait_for_timeout(1000)
        expect(page.locator("//*[@class='own-media__form-btn-wrapper']/button")).to_be_visible()
        page.wait_for_timeout(1000)
        page.locator(f"//ul/li[{i+1}]").click()
        page.wait_for_timeout(1000)

    page.reload()
    page.locator("//*[@class='p-multiselect-label']").click()
    page.wait_for_timeout(1000)
    page.locator("//div[@class='p-multiselect-panel p-component p-ripple-disabled']//div/div[@class='p-checkbox p-component']").click()
    page.wait_for_timeout(1000)
    page.locator("//*[@class='p-multiselect-close p-link']").click()
    page.wait_for_timeout(1000)

    """assert that inputs are visible, when all value of Brand"""
    expect(
        page.locator("//*[@class='p-dropdown-label p-inputtext'][text()='Select Existing Campaign']")).to_be_visible()
    make_screenshot(page, screenshot, item)


def test_open_campaign_dropdown_OG_18(use_google_auth) -> None:
    """OG - 18"""
    screenshot = 'manage_owned_media'
    item = 'existing_campaign'
    page = use_google_auth

    page.reload()
    page.wait_for_timeout(1200)
    # page.locator("//header//button[3]").click()
    # page.wait_for_timeout(1000)
    """he Campaign dropdown has at list one value: Select Existing Campaign"""
    explore_campaignfor_OG_18(page)
    """check Continue is visible"""
    expect(page.locator("//*[@class='own-media__form-btn-wrapper']/button")).to_be_visible()
    make_screenshot(page, screenshot, item)
    page.wait_for_timeout(1200)


def test_select_existing_campaign_and_validate_all_controls_on_the_page_OG_19(use_google_auth) -> None:
    """OG - 19"""
    screenshot = 'manage_owned_media'
    item = 'OG_19'
    page = use_google_auth
    page.reload()
    page.wait_for_timeout(1200)
    try:
        page.locator("//header//button[3]").click()
        page.wait_for_timeout(1000)
    except:
        pass

    """Campaign dropdown has at list one value: Select Existing Campaign"""
    explore_campaignfor_OG_18(page)

    """check dateRange fields"""
    for input in page.locator("//*[@id='dateRange']").all():
        expect(input).to_be_visible()
    page.wait_for_timeout(1000)

    """check CampaignPriority field equals 1"""
    assert page.locator("//div[@class='own-media__form-group'][4]/div/div/div/span").inner_text() == '4'

    """check CampaignPriority selectors"""
    campaign_priority_lst = ['1','2','3','4','5','6','7','8','9','10','1']
    for item in campaign_priority_lst:
        page.locator("//div[@class='own-media__form-group'][4]/div/div/div/span").click()
        page.get_by_role("option", name=item, exact=True).click()
        page.wait_for_timeout(700)

    """Media Type"""
    for item in campaign_priority_lst:
        page.locator("//div[@class='own-media__form-group'][4]/div/div/div/span").click()
        page.get_by_role("option", name=item, exact=True).click()
        page.wait_for_timeout(700)
        page.locator("//*[@class='select__container']/div[text()='Media Type']//following-sibling::*").click()
        page.get_by_role("option", name="web").click()
        page.wait_for_timeout(700)


    """Media Property"""
    media_property = ['VL Property', 'VL Media Property 01']
    for item in campaign_priority_lst:
        page.locator("//div[@class='own-media__form-group'][4]/div/div/div/span").click()
        page.get_by_role("option", name=item, exact=True).click()
        page.wait_for_timeout(700)
        page.locator("//*[@class='select__container']/div[text()='Media Type']//following-sibling::*").click()
        page.get_by_role("option", name="web").click()
        page.wait_for_timeout(700)
        for item in media_property:
            page.locator("//*[@class='select__container']/div[text()='Media Property']//following-sibling::*").click()
            page.get_by_role("option", name=item).click()
            page.wait_for_timeout(700)



    make_screenshot(page, screenshot,item)
    page.reload()
    page.wait_for_timeout(1200)


def test_existing_campaign_OG_20(use_google_auth) -> None:
    """OG - 20"""
    screenshot = 'manage_owned_media'
    item = 'OG_20'
    page = use_google_auth

    page.reload()
    page.wait_for_timeout(1200)
    try:
        page.locator("//header//button[3]").click()
        page.wait_for_timeout(1000)
    except:
        pass
    """expect Continue is disable"""

    page.wait_for_timeout(1200)
    expect(page.locator("//*[@class='own-media__form-btn-wrapper']/button")).to_be_disabled()
    """explore existing company"""
    explore_existing_campaign_OG_20(page)

    """validate that occasions is exist for campaign"""
    page.wait_for_timeout(3000)
    selector = page.locator("//div[@class='media__container grid-container__item']")
    """get occasionsResult & assert that is a list"""
    validate_data(selector)
    make_screenshot(page, screenshot, item)
    page.locator("//header//button[3]").click()
    page.wait_for_timeout(1000)


def test_user_returns_back_t_the_Fst_dialogue_OG_21(use_google_auth) -> None:
    """OG - 21"""
    screenshot = 'manage_owned_media'
    item = 'OG_21_1'
    item1 = 'OG_21_2'
    page = use_google_auth
    page.reload()
    page.wait_for_timeout(1200)
    # page.locator("//header//button[3]").click()
    # page.wait_for_timeout(1000)
    """explore existing company"""
    explore_existing_company(page)

    """validate that occasions is exist for campaign"""
    page.wait_for_timeout(3000)
    selector = page.locator("//div[@class='media__container grid-container__item']")
    """get occasionsResult & assert that is a list"""
    validate_data(selector)
    make_screenshot(page, screenshot,item)

    """click back and assert that it is start interFace"""
    page.locator("//span[@class='footer__back-text']").click()
    validate_start_interface(page)
    page.wait_for_timeout(1000)

    """click to continue"""
    page.get_by_role("button", name="Continue").click()
    page.wait_for_timeout(3000)
    elems = page.locator("//div[@class='media__container grid-container__item']")
    """get occasionsResult & assert that is a list"""
    validate_data(elems)
    """assert that length of selector and elems is equal """
    assert len(elems.all()) == len(selector.all())

    """click back and assert that it is start interFace"""
    page.locator("//span[@class='footer__back-text']").click()
    validate_start_interface(page)
    page.wait_for_timeout(1000)

    """change Campaign priority"""
    page.locator("//div[@class='own-media__form-group'][4]/div/div/div/span").click()
    page.get_by_role("option", name="4", exact=True).click()
    page.wait_for_timeout(700)

    """change media property"""
    page.locator("//*[@class='select__container']/div[text()='Media Property']//following-sibling::*").click()
    page.get_by_role("option", name="VL Media Property 01").click()
    page.wait_for_timeout(700)
    page.get_by_role("button", name="Continue").click()

    """validate that occasions is exist for campaign"""
    page.wait_for_timeout(3000)
    selector = page.locator("//div[@class='media__container grid-container__item']")
    """get occasionsResult & assert that is a list"""
    validate_data(selector)
    make_screenshot(page, screenshot, item1)
    page.locator("//header//button[3]").click()
    page.wait_for_timeout(1000)


def test_check_dialogue_linking_sections_occasions_OG_22(use_google_auth) -> None:
    """OG - 22"""
    screenshot = 'manage_owned_media'
    item = 'OG_22'
    breadcrumbs = 'TCCC ・ Sprite ・ VL New Camapign 2023-05-19 ・ web ・ VL Property'
    table_names = ['Section','Occasions', 'Priority',
                   'Default', 'Reach','Status','Action']
    page = use_google_auth

    page.reload()
    page.wait_for_timeout(1200)
    # page.locator("//header//button[3]").click()
    # page.wait_for_timeout(1000)
    """explore existing company"""
    explore_existing_company(page)

    """validate interFace"""
    page.wait_for_timeout(3000)
    """assert breadcrumbs"""
    assert page.locator("//*[@class='linking-occasions-header__campaign-param']").inner_text() == breadcrumbs

    """assert Available Sections"""
    expect(page.locator("//*[@class='available-sections__header']")).to_be_visible()
    expect(page.locator(("//div[@class='available-sections__radio-group']"))).to_be_visible()
    page.wait_for_timeout(1000)
    assert (len(page.locator("//*[@class='available-sections__radio-label']").all())) > 0
    make_screenshot(page, screenshot, item)

    """validate that occasions is exist for campaign"""
    selector = page.locator("//div[@class='media__container grid-container__item']")
    """get occasionsResult & assert that is a list"""
    validate_data(selector)

    """validate Review table"""
    validate_review_table(page, table_names)
    page.wait_for_timeout(1200)
    page.locator("//header//button[3]").click()
    page.wait_for_timeout(1000)


def test_select_new_section_and_occasion_and_link_OG_23(use_google_auth) -> None:
    """OG - 23"""
    screenshot = 'manage_owned_media'
    item = 'OG_23'
    num_of_occ = 8
    page = use_google_auth

    page.reload()
    page.wait_for_timeout(1200)
    try:
        page.locator("//header//button[3]").click()
        page.wait_for_timeout(1000)
    except:
        pass
    """explore existing company"""
    explore_existing_company(page)

    """unlink occ"""
    unlink(page)
    """click sections"""
    page.wait_for_timeout(3000)
    page.locator("//*[@class='available-sections__radio-label']/*[text()='About']").click()
    expect(page.locator("//*[@class='available-sections__radio-label']/*[text()='About']")).to_be_checked()
    page.wait_for_timeout(500)
    page.locator("//*[@class='available-sections__radio-label']/*[text()='Jogging']").click()
    expect(page.locator("//*[@class='available-sections__radio-label']/*[text()='About']")).not_to_be_checked()
    expect(page.locator("//*[@class='available-sections__radio-label']/*[text()='Jogging']")).to_be_checked()
    page.wait_for_timeout(1000)

    """link occasion"""
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ}]").click()
    page.wait_for_timeout(700)
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ}]").click()
    page.wait_for_timeout(2700)
    expect(page.locator("//*[@class='p-button p-component primary-btn linking-sections__link-button']")).not_to_be_visible()
    page.wait_for_timeout(700)

    """click all occasions"""
    elems = page.locator("//div[@class='media__container grid-container__item']").count()
    page.wait_for_timeout(1000)

    """click to all Unlinked occasions"""
    for item in range(elems):
        page.locator(f"//div[@class='media__container grid-container__item'][{item+1}]").click()
        page.wait_for_timeout(700)
    expect(page.locator("//*[@class='p-button p-component primary-btn linking-sections__link-button']")).to_be_visible()

    """unclik to all occasions"""
    for item in range(elems):
        page.locator(f"//div[@class='media__container grid-container__item'][{item+1}]").click()
        page.wait_for_timeout(700)
    expect(page.locator("//*[@class='p-button p-component primary-btn linking-sections__link-button']")).not_to_be_visible()

    """link occasion"""
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ}]").click()
    page.wait_for_timeout(700)
    page.locator("//*[@class='p-button p-component primary-btn linking-sections__link-button']").click()
    page.wait_for_timeout(2000)
    """click back return to Select Campaign"""
    page.locator("//span[@class='footer__back-text']").click()
    page.wait_for_timeout(700)

    explore_existing_company(page)
    page.wait_for_timeout(700)
    """go to  """
    page.locator("//*[@class='available-sections__radio-label']/*[text()='About']").click()
    page.wait_for_timeout(700)
    make_screenshot(page, screenshot, item)
    page.reload()
    # page.wait_for_timeout(1200)
    # page.locator("//span[@class='footer__back-text']").click()

    explore_existing_company(page)
    """unlink occasion"""
    page.locator("//tbody/tr//td/div/div[text()='Jogging']/following::td[@class='cell action left']/div/span").click()
    page.wait_for_timeout(1200)
    page.locator("//header//button[3]").click()
    page.wait_for_timeout(1000)



def test_select_new_section_OG_24(use_google_auth) -> None:
    """OG - 24"""
    screenshot = 'manage_owned_media'
    item = 'OG_24'
    page = use_google_auth

    page.reload()
    page.wait_for_timeout(1200)
    # page.locator("//header//button[3]").click()
    # page.wait_for_timeout(1000)
    """explore existing company"""
    explore_existing_company(page)

    """validate that occasions is exist for campaign"""
    page.wait_for_timeout(3000)
    selector = page.locator("//div[@class='media__container grid-container__item']")
    """get occasionsResult & assert that is a list"""
    validate_data(selector)

    """click sections"""
    page.wait_for_timeout(1000)
    page.locator("//*[@class='available-sections__radio-label']/*[text()='About']").click()
    expect(page.locator("//*[@class='available-sections__radio-label']/*[text()='About']")).to_be_checked()
    page.wait_for_timeout(1000)

    page.locator("//*[@class='available-sections__radio-label']/*[text()='Jogging']").click()
    expect(page.locator("//*[@class='available-sections__radio-label']/*[text()='Jogging']")).to_be_checked()
    expect(page.locator("//*[@class='available-sections__radio-label']/*[text()='About']")).not_to_be_checked()
    page.wait_for_timeout(1000)
    #
    # page.locator("//*[@class='available-sections__radio-label']/*[text()='Super Section']").click()
    # expect(page.locator("//*[@class='available-sections__radio-label']/*[text()='Super Section']")).to_be_checked()
    # expect(page.locator("//*[@class='available-sections__radio-label']/*[text()='Jogging']")).not_to_be_checked()

    # page.locator("//*[@class='available-sections__radio-label']/*[text()='about sec']").click()
    # expect(page.locator("//*[@class='available-sections__radio-label']/*[text()='about sec']")).to_be_checked()
    # expect(page.locator("//*[@class='available-sections__radio-label']/*[text()='Super Section']")).not_to_be_checked()
    page.wait_for_timeout(1000)
    page.locator("//header//button[3]").click()
    page.wait_for_timeout(1000)



def test_check_section_modal_OG_26(use_google_auth) -> None:
    """OG - 26"""
    screenshot = 'manage_owned_media'
    item = 'OG_26'
    num_of_occ = 19
    page = use_google_auth
    page.reload()
    page.wait_for_timeout(1200)
    try:
        page.locator("//header//button[3]").click()
        page.wait_for_timeout(1000)
    except:
        pass
    """explore existing company"""
    explore_existing_company(page)

    """validate that occasions is exist for campaign"""
    page.wait_for_timeout(3000)
    selector = page.locator("//div[@class='media__container grid-container__item']")
    """get occasionsResult & assert that is a list"""
    validate_data(selector)
    unlink(page)

    page.wait_for_timeout(1000)
    page.locator("//*[@class='available-sections__radio-label']/*[text()='About']").click()
    """link occasion"""
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ}]").click()
    page.locator("//div[@class='linking-sections__upper-content']/button").click()
    page.wait_for_timeout(1000)

    """click to firth pencil"""
    page.locator("//tbody/tr//td/div/div[text()='About']//following-sibling::*").click()
    page.wait_for_timeout(2000)

    """validate section modal"""
    # 1 column
    expect(page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td/*[@class='p-icon p-datatable-reorderablerow-handle']")).to_be_visible()
    # 2 column
    expect(page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[2]")).to_be_visible()
    # 3 column
    expect(page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[@class='cell occasion-title left']/div/div/i")).to_be_visible()
    # 4 column
    expect(page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[3]")).to_be_visible()
    # 5 column
    expect(page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[4]")).to_be_visible()
    # 6 column
    expect(page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[5]")).to_be_visible()
    make_screenshot(page, screenshot, item)

    """click to Occasion modal from section"""
    page.locator("//*[@class='p-sidebar-content']//table//i").click()
    page.wait_for_timeout(1000)
    validate_right_side_bar(page)
    """click cancel"""
    page.locator("//*[@class='occasion-drawer__footer-wrapper']//button[1]").click()
    page.wait_for_timeout(1000)
    # """discard"""
    # page.locator("//*[@class='p-button p-component small primary-btn']").click()
    # page.wait_for_timeout(1000)

    """close modals click X"""
    page.locator("//*[@class='p-sidebar-close p-sidebar-icon p-link']").click()


    """unlink occasion"""
    page.locator("//tbody/tr//td/div/div[text()='About']/following::td[@class='cell action left']/div/span").click()
    page.wait_for_timeout(1200)
    page.locator("//header//button[3]").click()
    page.wait_for_timeout(1000)



def test_check_inputs_occasion_modal_OG_27(use_google_auth) -> None:
    """OG - 27"""
    screenshot = 'manage_owned_media'
    item = 'OG_27_1'
    item1 = 'OG_27_2'
    num_of_occ = 7
    current_date = datetime.now()
    start_day = int(current_date.day)
    stop_day = int(start_day) + 1

    item = f"{start_day}_{stop_day}"
    page = use_google_auth

    page.reload()
    page.wait_for_timeout(1200)
    try:
        page.locator("//header//button[3]").click()
        page.wait_for_timeout(1000)
    except:
        pass
    """explore existing company"""
    explore_existing_company(page)

    """validate that occasions is exist for campaign"""
    page.wait_for_timeout(3600)
    selector = page.locator("//div[@class='media__container grid-container__item']")
    """get occasionsResult & assert that is a list"""
    validate_data(selector)

    """unlink"""
    unlink(page)

    """click section"""
    page.wait_for_timeout(1000)
    page.locator("//*[@class='available-sections__radio-label']/*[text()='About']").click()

    """link occasion"""
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ}]").click()
    page.locator("//div[@class='linking-sections__upper-content']/button").click()
    page.wait_for_timeout(1000)

    """click to pencil for open section modal"""
    page.locator("//tbody/tr//td/div/div[text()='About']//following-sibling::*").click()
    page.wait_for_timeout(1000)

    """click to pencil for open occasion modal"""
    page.wait_for_timeout(1300)
    page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[@class='cell occasion-title left']/div/div/i").click()
    page.wait_for_timeout(3000)

    """validate occasion modal"""
    validate_right_side_bar(page)

    """click to markets input and try to execute Clear all"""
    page.locator("//*[@class='p-treeselect p-component p-inputwrapper p-treeselect-chip p-inputwrapper-filled']").click()
    page.get_by_role("button", name="Clear All").click()
    page.wait_for_timeout(1000)
    page.locator("//*[@class='p-button p-component transparent primary-btn']").click()
    page.wait_for_timeout(1000)
    page.locator("//div[@class='p-sidebar-header']//span[@class='occasion-drawer__header']").click()
    page.wait_for_timeout(1000)
    page.locator("//*[@class='p-treeselect-label p-placeholder']").click()
    page.wait_for_timeout(1000)
    page.locator("//div[@class='p-sidebar-header']//span[@class='occasion-drawer__header']").click()

    """explore options for OCC"""
    explore_occ_modal_inputs(page, start_day, stop_day)
    make_screenshot(page, screenshot, item)
    """click apply and confirm for chosen options"""
    #  apply
    page.locator("//*[@class='p-button p-component primary-btn']").click()
    page.wait_for_timeout(30000)
    # confirm
    page.locator("//*[@class='p-button p-component primary-btn']").click()
    page.wait_for_timeout(10000)

    """open Occ modal"""
    page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[@class='cell occasion-title left']/div/div/i").click()
    page.wait_for_timeout(3000)
    validate_updated_occ_after_confirm(page)
    make_screenshot(page, screenshot, item1)
    page.wait_for_timeout(1000)
    """unlink"""
    unlink(page)
    page.locator("//header//button[3]").click()
    page.wait_for_timeout(1000)



def test_check_table_linked_occ_sec_for_group_occ_by_one_sec_OG_28(use_google_auth) -> None:
    """OG - 28"""
    screenshot = 'manage_owned_media'
    item = ['OG_28_1','OG_28_2','OG_28_3']
    num_of_occ = 16
    table_names = ['Section','Occasions', 'Priority',
                   'Default', 'Reach','Status','Action']
    list_of_priority_default = ["1","2","3","4"]
    page = use_google_auth

    page.reload()
    page.wait_for_timeout(1200)
    try:
        page.locator("//header//button[3]").click()
        page.wait_for_timeout(1000)
    except:
        pass
    """explore existing company"""
    explore_existing_company(page)

    """validate that occasions is exist for campaign"""
    page.wait_for_timeout(6000)
    selector = page.locator("//div[@class='media__container grid-container__item']")
    """get occasionsResult & assert that is a list"""
    validate_data(selector)

    """unlink occasion"""
    unlink(page)

    """link occasion"""
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ}]").click()
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ-1}]").click()
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ+1}]").click()
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ-2}]").click()
    page.locator("//div[@class='linking-sections__upper-content']/button").click()
    page.wait_for_timeout(15000)

    """validate review table"""
    validate_review_table(page, table_names)

    """validate Priority"""
    page.wait_for_timeout(2000)
    elems_of_priority = page.locator("//table//div[@class='p-column-header-content']/span[text()='Priority']/following::td[@class='cell occasion-priority right']/div")
    validate_priority(elems_of_priority, list_of_priority_default)
    page.wait_for_timeout(700)

    """click to priority"""
    page.locator("//table//th[3]/div/span[@class='p-column-title']").click()
    page.wait_for_timeout(1000)
    page.locator("//table//th[3]/div/span[@class='p-column-title']").click()
    page.wait_for_timeout(2000)

    """validate changed priority"""
    validate_priority(elems_of_priority, list_of_priority_default[::-1])
    page.wait_for_timeout(2000)
    make_screenshot(page, screenshot, item[0])

    """validate default check box is only one for table"""
    expect(page.locator("//table//tr[1]//td[@class='cell occasion-default']//input")).not_to_be_checked()
    expect(page.locator("//table//tr[2]//td[@class='cell occasion-default']//input")).not_to_be_checked()
    expect(page.locator("//table//tr[3]//td[@class='cell occasion-default']//input")).not_to_be_checked()
    expect(page.locator("//table//tr[4]//td[@class='cell occasion-default']//input")).to_be_checked()

    """click to change default"""
    page.locator("//table//tr[2]//td[@class='cell occasion-default']").click()
    page.locator("//table//tr[2]//td[@class='cell occasion-default']").click()
    page.wait_for_timeout(1000)
    expect(page.locator("//table//tr[2]//td[@class='cell occasion-default']//input")).to_be_checked()
    page.wait_for_timeout(1200)

    page.locator("//table//tr[3]//td[@class='cell occasion-default']").click()
    page.wait_for_timeout(1000)
    expect(page.locator("//table//tr[3]//td[@class='cell occasion-default']//div[2]")).to_be_visible()
    page.wait_for_timeout(1000)

    page.locator("//table//tr[4]//td[@class='cell occasion-default']").click()
    page.wait_for_timeout(1000)
    expect(page.locator("//table//tr[4]//td[@class='cell occasion-default']//div[2]")).to_be_visible()
    page.wait_for_timeout(1000)

    page.locator("//table//tr[1]//td[@class='cell occasion-default']").click()
    expect(page.locator("//table//tr[1]//td[@class='cell occasion-default']//input")).to_be_checked()
    make_screenshot(page, screenshot, item[1])

    """click Reach"""
    page.locator("//table//th[@class='cell occasion-instance-reach right p-sortable-column']").click()
    page.wait_for_timeout(1200)
    """validate reach values"""
    elems_of_reach = page.locator("//table//div[@class='p-column-header-content']/span[text()='Reach']/following::td[@class='cell occasion-instance-reach right']/div").all()
    validate_reach_reneview_table(elems_of_reach, flag=0)
    page.wait_for_timeout(1200)
    page.locator("//table//th[@class='cell occasion-instance-reach right p-sortable-column p-highlight']").click()
    validate_reach_reneview_table(elems_of_reach, flag=1)
    page.wait_for_timeout(1200)
    make_screenshot(page, screenshot, item[2])

    page.locator("//table//th[3]/div/span[@class='p-column-title']").click()
    page.wait_for_timeout(2000)
    validate_priority(elems_of_priority, list_of_priority_default)
    page.wait_for_timeout(1200)

    """unlink occasion"""
    unlink(page)
    page.locator("//header//button[3]").click()
    page.wait_for_timeout(1000)



def test_check_table_linked_occ_for_group_occ_by_few_sections_OG_29(use_google_auth) -> None:
    """OG - 29"""
    screenshot = 'manage_owned_media'
    item = ['OG_29_1','OG_29_2','OG_29_3']
    num_of_occ = 6
    table_names = ['Section','Occasions', 'Priority',
                   'Default', 'Reach','Status','Action']
    list_of_priority_default = ["1","2","1","2"]
    list_of_priority_default_changed = ['2','1','2','1']
    page = use_google_auth

    page.reload()
    try:
        page.wait_for_timeout(1200)
        page.locator("//header//button[3]").click()
    except:
        pass
    page.wait_for_timeout(1000)
    """explore existing company"""
    explore_existing_company(page)

    page.wait_for_timeout(6000)
    selector = page.locator("//div[@class='media__container grid-container__item']")
    """get occasionsResult & assert that is a list"""
    validate_data(selector)

    """unlink occasion"""
    unlink(page)
    """link occasion for default section"""
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ}]").click()
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ+1}]").click()
    page.wait_for_timeout(1000)
    page.locator("//div[@class='linking-sections__upper-content']/button").click()
    page.wait_for_timeout(8000)

    """click to next section"""
    page.locator("//*[@class='available-sections__radio-label']/*[text()='Jogging']").click()
    """link for next section"""
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ}]").click()
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ+1}]").click()
    page.wait_for_timeout(1000)
    page.locator("//div[@class='linking-sections__upper-content']/button").click()
    page.wait_for_timeout(8000)

    """validate review table"""
    validate_review_table(page, table_names)

    """validate Priority"""
    page.wait_for_timeout(2000)
    elems_of_priority = page.locator("//table//div[@class='p-column-header-content']/span[text()='Priority']/following::td[@class='cell occasion-priority right']/div")
    validate_priority(elems_of_priority, list_of_priority_default)
    page.wait_for_timeout(700)

    """click to priority"""
    page.locator("//table//th[3]/div/span[@class='p-column-title']").click()
    page.wait_for_timeout(1000)
    page.locator("//table//th[3]/div/span[@class='p-column-title']").click()
    page.wait_for_timeout(2000)


    """validate changed priority"""
    validate_priority(elems_of_priority, list_of_priority_default_changed)
    page.wait_for_timeout(2000)
    make_screenshot(page, screenshot, item[0])

    """validate default check box is checked by default at table"""
    expect(page.locator("//table//tr[1]//td[@class='cell occasion-default']//input")).not_to_be_checked()
    expect(page.locator("//table//tr[2]//td[@class='cell occasion-default']//input")).to_be_checked()
    expect(page.locator("//table//tr[3]//td[@class='cell occasion-default']//input")).not_to_be_checked()
    expect(page.locator("//table//tr[4]//td[@class='cell occasion-default']//input")).to_be_checked()

    """click to change default and assert"""
    page.locator("//table//tr[1]//td[@class='cell occasion-default']//div[2]").click()
    page.locator("//table//tr[1]//td[@class='cell occasion-default']//div[2]").click()
    page.wait_for_timeout(2000)
    expect(page.locator("//table//tr[1]//td[@class='cell occasion-default']//input")).to_be_checked()
    expect(page.locator("//table//tr[2]//td[@class='cell occasion-default']//input")).not_to_be_checked()
    page.locator("//table//tr[3]//td[@class='cell occasion-default']//div[2]").click()
    expect(page.locator("//table//tr[2]//td[@class='cell occasion-default']//input")).not_to_be_checked()
    expect(page.locator("//table//tr[3]//td[@class='cell occasion-default']//input")).to_be_checked()
    expect(page.locator("//table//tr[4]//td[@class='cell occasion-default']//input")).not_to_be_checked()

    """click Reach"""
    page.locator("//table//th[@class='cell occasion-instance-reach right p-sortable-column']").click()
    page.wait_for_timeout(1200)
    """validate reach values"""
    elems_of_reach = page.locator("//table//div[@class='p-column-header-content']/span[text()='Reach']/following::td[@class='cell occasion-instance-reach right']/div").all()
    validate_reach_reneview_table_for_few_sections(elems_of_reach, flag=0)
    page.wait_for_timeout(1200)
    page.locator("//table//th[@class='cell occasion-instance-reach right p-sortable-column p-highlight']").click()
    validate_reach_reneview_table_for_few_sections(elems_of_reach, flag=1)
    page.wait_for_timeout(1200)
    make_screenshot(page, screenshot, item[2])

    """click to priority"""
    page.locator("//table//th[3]/div/span[@class='p-column-title']").click()
    page.wait_for_timeout(1000)

    """validate Priority"""
    page.wait_for_timeout(2000)
    elems_of_priority = page.locator("//table//div[@class='p-column-header-content']/span[text()='Priority']/following::td[@class='cell occasion-priority right']/div")
    validate_priority(elems_of_priority, list_of_priority_default)
    page.wait_for_timeout(700)


    """unlink occasion"""
    unlink(page)
    page.locator("//header//button[3]").click()
    page.wait_for_timeout(1000)



def test_check_default_ield_in_section_modal_OG_30(use_google_auth) -> None:
    """OG - 30"""
    screenshot = 'manage_owned_media'
    item = ['OG_30_1','OG_30_2','OG_30_3']
    num_of_occ = 6
    table_names = ['Occasions','Priority','Default','Reach']
    list_of_priority_default = ['1','2','3']
    page = use_google_auth
    page.reload()
    try:
        page.wait_for_timeout(1200)
        page.locator("//header//button[3]").click()
    except:
        pass
    page.wait_for_timeout(1000)
    """explore existing company"""
    explore_existing_company(page)

    page.wait_for_timeout(6000)
    selector = page.locator("//div[@class='media__container grid-container__item']")
    """get occasionsResult & assert that is a list"""
    validate_data(selector)

    """unlink occasion"""
    unlink(page)
    """link occasion for default section"""
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ}]").click()
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ-1}]").click()
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ+1}]").click()
    page.wait_for_timeout(1000)
    page.locator("//div[@class='linking-sections__upper-content']/button").click()
    page.wait_for_timeout(8000)

    """click to pencil for open section modal"""
    page.locator("//tbody/tr//td/div/div[text()='About']//following-sibling::*").click()
    page.wait_for_timeout(2000)

    """validate section modal"""
    elems_of_table = page.locator("//div[@class='p-sidebar-content']//table//th/div/span").all()
    count = 0
    for i in elems_of_table:
        assert i.inner_text() == table_names[count]
        count += 1

    """validate filed fields in section"""
    # 1 column
    elems_of_humburger = page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td/*[@class='p-icon p-datatable-reorderablerow-handle']").all()
    elems_of_occ_name = page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[2]").all()
    elems_of_occ_pencil = page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[@class='cell occasion-title left']/div/div/i").all()
    elems_of_priority = page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[3]").all()
    elems_of_default = page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[4]").all()
    elems_of_reach = page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[5]").all()
    for elem in elems_of_humburger:
        expect(elem).to_be_visible()

    # 2 column
    for elem in elems_of_occ_name:
        expect(elem).to_be_visible()

    # 3 column
    for elem in elems_of_occ_pencil:
        expect(elem).to_be_visible()

    # 4 column
    for elem in elems_of_priority:
        expect(elem).to_be_visible()

    # 5 column
    for elem in elems_of_default:
        expect(elem).to_be_visible()

    # 6 column
    for elem in elems_of_reach:
        expect(elem).to_be_visible()
    make_screenshot(page, screenshot, item[0])

    """validate that default is on;y one"""
    expect(page.locator("//div[@class='p-sidebar-content']//table//tr[1]//td[@class='cell occasion-default']//input")).to_be_checked()
    expect(page.locator("//div[@class='p-sidebar-content']//table//tr[2]//td[@class='cell occasion-default']//input")).not_to_be_checked()
    expect(page.locator("//div[@class='p-sidebar-content']//table//tr[3]//td[@class='cell occasion-default']//input")).not_to_be_checked()

    """click to next default and assert"""
    page.locator("//div[@class='p-sidebar-content']//table//tr[2]//td[@class='cell occasion-default']").click()
    page.wait_for_timeout(2000)
    expect(page.locator("//div[@class='p-sidebar-content']//table//tr[2]//td[@class='cell occasion-default']//input")).to_be_checked()
    expect(page.locator("//div[@class='p-sidebar-content']//table//tr[1]//td[@class='cell occasion-default']//input")).not_to_be_checked()
    expect(page.locator("//div[@class='p-sidebar-content']//table//tr[3]//td[@class='cell occasion-default']//input")).not_to_be_checked()
    """next click default"""
    page.locator("//div[@class='p-sidebar-content']//table//tr[3]//td[@class='cell occasion-default']").click()
    page.wait_for_timeout(2000)
    expect(page.locator("//div[@class='p-sidebar-content']//table//tr[3]//td[@class='cell occasion-default']//input")).to_be_checked()
    expect(page.locator("//div[@class='p-sidebar-content']//table//tr[1]//td[@class='cell occasion-default']//input")).not_to_be_checked()
    expect(page.locator("//div[@class='p-sidebar-content']//table//tr[2]//td[@class='cell occasion-default']//input")).not_to_be_checked()

    """click confirm at section edit"""
    page.locator("//div[@class='side-panel__footer-buttons']/button[@class='p-button p-component primary-btn']").click()
    page.wait_for_timeout(4000)

    """validate Priority"""
    page.wait_for_timeout(2000)
    elems_of_priority = page.locator("//table//div[@class='p-column-header-content']/span[text()='Priority']/following::td[@class='cell occasion-priority right']/div")
    validate_priority(elems_of_priority, list_of_priority_default)
    page.wait_for_timeout(700)

    """validate default"""
    expect(page.locator("//table//tr[1]//td[@class='cell occasion-default']//input")).not_to_be_checked()
    expect(page.locator("//table//tr[2]//td[@class='cell occasion-default']//input")).not_to_be_checked()
    expect(page.locator("//table//tr[3]//td[@class='cell occasion-default']//input")).to_be_checked()

    """unlink occasion"""
    unlink(page)
    page.locator("//header//button[3]").click()
    page.wait_for_timeout(1000)



def test_check_unlink_field_and_download_csv_for_all_occ_OG_31(use_google_auth) -> None:
    """OG - 31"""
    screenshot = 'manage_owned_media'
    item = ['OG_31_1','OG_31_2']
    num_of_occ = 6
    page = use_google_auth
    page.reload()
    try:
        page.wait_for_timeout(1200)
        page.locator("//header//button[3]").click()
    except:
        pass
    page.wait_for_timeout(1000)
    """explore existing company"""
    explore_existing_company(page)

    page.wait_for_timeout(6000)
    selector = page.locator("//div[@class='media__container grid-container__item']")
    """get occasionsResult & assert that is a list"""
    validate_data(selector)

    """unlink occasion"""
    unlink(page)
    """link occasion for default section"""
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ}]").click()
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ+1}]").click()
    page.wait_for_timeout(1000)
    page.locator("//div[@class='linking-sections__upper-content']/button").click()
    page.wait_for_timeout(8000)

    """click to next section"""
    page.locator("//*[@class='available-sections__radio-label']/*[text()='Jogging']").click()
    """link for next section"""
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ}]").click()
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ+1}]").click()
    page.wait_for_timeout(1000)
    page.locator("//div[@class='linking-sections__upper-content']/button").click()
    page.wait_for_timeout(8000)

    """click to download csv"""
    download_csv(page)
    page.wait_for_timeout(1000)
    make_screenshot(page, screenshot, item[0])
    """validate csv"""
    validate_csv(flag=0)

    """unlink occasion"""
    unlink(page)
    page.wait_for_timeout(1000)
    """dowload new csv"""
    download_csv(page)
    make_screenshot(page, screenshot, item[1])
    """validate csv"""
    validate_csv(flag=1)
    """go to OWM"""
    page.locator("//header//button[3]").click()
    page.wait_for_timeout(1000)



def test_check_section_modal_is_close_without_save_changes_OG_32(use_google_auth) -> None:
    """OG - 32"""
    screenshot = 'manage_owned_media'
    item = ['OG_32_1','OG_32_2','OG_32_3']
    num_of_occ = 11
    page = use_google_auth
    page.reload()
    try:
        page.wait_for_timeout(1200)
        page.locator("//header//button[3]").click()
    except:
        pass
    page.wait_for_timeout(1000)
    """explore existing company"""
    explore_existing_company(page)

    page.wait_for_timeout(6000)
    selector = page.locator("//div[@class='media__container grid-container__item']")
    """get occasionsResult & assert that is a list"""
    validate_data(selector)
    unlink(page)

    page.wait_for_timeout(1000)
    page.locator("//*[@class='available-sections__radio-label']/*[text()='About']").click()
    """link occasion"""
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ}]").click()
    page.locator("//div[@class='linking-sections__upper-content']/button").click()
    page.wait_for_timeout(1000)

    """click to firth pencil"""
    page.locator("//tbody/tr//td/div/div[text()='About']//following-sibling::*").click()
    page.wait_for_timeout(2000)

    """validate section modal"""
    # 1 column
    expect(page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td/*[@class='p-icon p-datatable-reorderablerow-handle']")).to_be_visible()
    # 2 column
    expect(page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[2]")).to_be_visible()
    # 3 column
    expect(page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[@class='cell occasion-title left']/div/div/i")).to_be_visible()
    # 4 column
    expect(page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[3]")).to_be_visible()
    # 5 column
    expect(page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[4]")).to_be_visible()
    # 6 column
    expect(page.locator("//div[@class='p-sidebar-content']//*[@class='p-datatable-tbody']/tr/td[5]")).to_be_visible()
    make_screenshot(page, screenshot, item[0])

    """click x to close section edit"""
    page.locator("//*[@class='p-sidebar-close p-sidebar-icon p-link']").click()
    validate_data(selector)

    """click to firth pencil"""
    page.locator("//tbody/tr//td/div/div[text()='About']//following-sibling::*").click()
    page.wait_for_timeout(2000)
    make_screenshot(page, screenshot, item[1])

    """click cancel to section edit"""
    page.get_by_text('Cancel').click()
    validate_data(selector)

    """click to firth pencil"""
    page.locator("//tbody/tr//td/div/div[text()='About']//following-sibling::*").click()
    page.wait_for_timeout(2000)
    make_screenshot(page, screenshot, item[2])

    """click to outside"""
    page.mouse.click(300, 405)
    validate_data(selector)
    page.wait_for_timeout(2000)

    """unlink"""
    unlink(page)
    page.wait_for_timeout(2000)
    """go to OWM"""
    page.locator("//header//button[3]").click()
    page.wait_for_timeout(1000)



def test_check_occ_modal_is_close_without_save_changes_OG_33(use_google_auth) -> None:
    """OG - 33"""
    screenshot = 'manage_owned_media'
    item = ['OG_33_1','OG_33_2']
    num_of_occ = 19
    page = use_google_auth
    page.reload()
    page.wait_for_timeout(1200)
    try:
        page.locator("//header//button[3]").click()
        page.wait_for_timeout(1000)
    except:
        pass
    """explore existing company"""
    explore_existing_company(page)

    """validate that occasions is exist for campaign"""
    page.wait_for_timeout(3000)
    selector = page.locator("//div[@class='media__container grid-container__item']")
    """get occasionsResult & assert that is a list"""
    validate_data(selector)
    unlink(page)

    page.wait_for_timeout(1000)
    page.locator("//*[@class='available-sections__radio-label']/*[text()='About']").click()
    """link occasion"""
    page.locator(f"//div[@class='media__container grid-container__item'][{num_of_occ}]").click()
    page.locator("//div[@class='linking-sections__upper-content']/button").click()
    page.wait_for_timeout(1000)

    """click to Occasion modal from section"""
    page.locator("//*[@class='cell occasion-title left']//i").click()
    page.wait_for_timeout(1000)
    validate_right_side_bar(page)

    """click cancel"""
    page.locator("//*[@class='occasion-drawer__footer-wrapper']//button[1]").click()
    make_screenshot(page, screenshot, item[0])
    page.wait_for_timeout(1000)
    # """discard"""
    # page.locator("//*[@class='p-button p-component small primary-btn']").click()
    # page.wait_for_timeout(1000)

    """click to Occasion modal from section"""
    page.locator("//*[@class='cell occasion-title left']//i").click()
    page.wait_for_timeout(1000)
    validate_right_side_bar(page)

    """close modals click X"""
    page.locator("//*[@class='p-sidebar-close p-sidebar-icon p-link']").click()
    make_screenshot(page, screenshot, item[1])
    page.wait_for_timeout(1000)

    """click to Occasion modal from section"""
    page.locator("//*[@class='cell occasion-title left']//i").click()
    page.wait_for_timeout(1000)
    validate_right_side_bar(page)

    """click to outside"""
    page.mouse.click(300, 405)
    validate_data(selector)
    page.wait_for_timeout(2000)

    """unlink"""
    unlink(page)
    page.wait_for_timeout(2000)
    """go to OWM"""
    page.locator("//header//button[3]").click()
    page.wait_for_timeout(1000)





