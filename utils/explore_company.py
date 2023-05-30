from conftest import OMM_CAMPAIGN
from playwright.sync_api import expect

def explore_existing_company(page):
    page.wait_for_timeout(500)
    page.locator("//*[@class='own-media__form-group'][1]/div/div").click()
    page.get_by_role("option", name="Select Existing Campaign").click()
    page.wait_for_timeout(500)
    page.locator("//*[@class='own-media__form-group'][2]/div/div").click()
    page.get_by_role("option", name=OMM_CAMPAIGN).click()
    page.wait_for_timeout(500)
    page.locator("//*[@class='select__container']/div[text()='Media Type']//following-sibling::*").click()
    page.get_by_role("option", name="web").click()
    page.locator("//*[@class='select__container']/div[text()='Media Property']//following-sibling::*").click()
    page.get_by_role("option", name="VL Property").click()
    page.get_by_role("button", name="Continue").click()

def explore_campaignfor_OG_18(page):
    """for OG-18"""
    page.wait_for_timeout(500)
    page.locator("//*[@class='own-media__form-group'][1]/div/div").click()
    page.get_by_role("option", name="Select Existing Campaign").click()
    page.wait_for_timeout(500)
    page.locator("//*[@class='own-media__form-group'][2]/div/div").click()
    page.get_by_role("option", name=OMM_CAMPAIGN).click()
    page.wait_for_timeout(500)
    

def explore_occ_modal_inputs(page, start_day, stop_day):
    """choose date input"""
    page.get_by_placeholder("Select Date Range").click()
    page.get_by_role("button", name="Previous Month").click()
    page.get_by_role("button", name="Previous Month").click()
    page.get_by_role("button", name="Previous Month").click()

    page.get_by_role("gridcell", name=str(start_day), exact=True).locator("span").click()
    page.get_by_text(str(stop_day)).click()
    page.get_by_role("button", name="OK").click()
    page.wait_for_timeout(1000)

    """choose week days"""
    page.locator("//*[@class='select__title'][text()='Week Days']/following::div[@class='p-multiselect-label'][1]").click()
    page.wait_for_timeout(1000)
    page.get_by_role("option", name="Wednesday").locator("span").first.click()
    page.wait_for_timeout(1000)
    page.get_by_role("option", name="Thursday").locator("span").first.click()
    page.wait_for_timeout(1000)
    page.locator("div").filter(has_text="9 results are availableMondayTuesdayWednesdayThursdayFridaySaturdaySundayWeekday").get_by_role("button", name="Close").click()
    page.wait_for_timeout(1000)

    """choose days parts"""
    page.locator("//*[@class='select__title'][text()='Week Days']/following::div[@class='p-multiselect-label'][2]").click()
    page.wait_for_timeout(1000)
    page.get_by_role("option", name="midday").locator("span").first.click()
    page.wait_for_timeout(1000)
    page.get_by_role("option", name="afternoon").locator("span").first.click()
    page.wait_for_timeout(1000)
    page.locator("div").filter(has_text="7 results are availableearly morningmid-morningmiddayafternoonearly eveningeveni").get_by_role("button", name="Close").click()
    page.wait_for_timeout(1000)


def explore_existing_campaign_OG_20(page):
    page.wait_for_timeout(500)
    page.locator("//*[@class='own-media__form-group'][1]/div/div").click()
    page.get_by_role("option", name="Select Existing Campaign").click()
    page.wait_for_timeout(500)
    page.locator("//*[@class='own-media__form-group'][2]/div/div").click()
    page.get_by_role("option", name=OMM_CAMPAIGN).click()
    """expect Continue is disable"""
    expect(page.locator("//*[@class='own-media__form-btn-wrapper']/button")).to_be_disabled()
    page.wait_for_timeout(500)
    page.locator("//*[@class='select__container']/div[text()='Media Type']//following-sibling::*").click()
    page.get_by_role("option", name="web").click()
    """expect Continue is disable"""
    expect(page.locator("//*[@class='own-media__form-btn-wrapper']/button")).to_be_disabled()
    page.locator("//*[@class='select__container']/div[text()='Media Property']//following-sibling::*").click()
    page.get_by_role("option", name="VL Media Property 01").click()
    page.get_by_role("button", name="Continue").click()

def download_csv(page):
    with page.expect_download() as download_info:
        page.get_by_text("Download CSV").click()
    file = download_info.value
    file.save_as('./utils/csv/test_omm.csv')