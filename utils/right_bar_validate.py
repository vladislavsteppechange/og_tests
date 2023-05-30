from playwright.sync_api import expect


def validate_right_side_bar(page):
    expect(page.locator("//div[@class='p-sidebar-header']//span[@class='occasion-drawer__header']")).to_be_visible()
    # """Markets drop down is visible"""
    expect(page.locator("//div[@class='selector-group__title']")).to_be_visible()
    """time range section & it dropdowns is visible"""
    expect(page.locator("//div[@class='time-range selector-group']")).to_be_visible()
    """date input"""
    expect(page.locator("//input[@id='dateRange']")).to_be_visible()
    """div time-range which contains all input fields"""
    expect(page.locator("//div[@class='time-range__selectors']")).to_be_visible()
    """week days input check"""
    expect(page.locator("//*[@class='select__title'][text()='Week Days']/following::div[@class='p-multiselect-label'][1]")).to_be_visible()
    """day parts input check"""
    expect(page.locator("//*[@class='select__title'][text()='Week Days']/following::div[@class='p-multiselect-label'][2]")).to_be_visible()
    """left canvas check"""
    page.locator("//*[@class='chart-container']").click()
    """right canvas check"""
    page.locator("//*[@class='mapboxgl-canvas-container mapboxgl-interactive mapboxgl-touch-drag-pan mapboxgl-touch-zoom-rotate']/canvas").click()


def validate_start_interface(page):
    interface_tittle = 'Select Campaign'
    title_selector = page.locator("//*[@class='own-media__title']").inner_text()
    assert title_selector == interface_tittle

def validate_updated_occ_after_confirm(page):
    """assert that, occasion has been updated"""

    # click to Week days input
    page.locator("//*[@class='select__title'][text()='Week Days']/following::div[@class='p-multiselect-label'][1]").click()
    page.wait_for_timeout(1000)
    expect(page.locator("//ul//li[1]//*[@class='p-checkbox-box p-highlight']")).to_be_visible()
    expect(page.locator("//ul//li[2]//*[@class='p-checkbox-box p-highlight']")).to_be_visible()
    expect(page.locator("//ul//li[3]//*[@class='p-checkbox-box']")).to_be_visible()
    page.wait_for_timeout(500)
    expect(page.locator("//ul//li[4]//*[@class='p-checkbox-box']")).to_be_visible()
    page.wait_for_timeout(1000)
    expect(page.locator("//ul//li[5]//*[@class='p-checkbox-box p-highlight']")).to_be_visible()

    # click to Day parts input
    page.locator("//*[@class='select__title'][text()='Week Days']/following::div[@class='p-multiselect-label'][2]").click()
    page.wait_for_timeout(1000)
    expect(page.locator("//ul//li[1]//*[@class='p-checkbox-box p-highlight']")).to_be_visible()
    expect(page.locator("//ul//li[2]//*[@class='p-checkbox-box p-highlight']")).to_be_visible()
    expect(page.locator("//ul//li[3]//*[@class='p-checkbox-box']")).to_be_visible()
    page.wait_for_timeout(500)
    expect(page.locator("//ul//li[4]//*[@class='p-checkbox-box']")).to_be_visible()
    page.wait_for_timeout(1000)
    expect(page.locator("//ul//li[5]//*[@class='p-checkbox-box p-highlight']")).to_be_visible()

