
def unlink_occasins(page):
    page.wait_for_selector("//tbody/tr/td[7]")
    if page.locator("//span[text()='Unlink']").count() > 0:
        for i in page.locator("//*[text()='Unlink']", has_text='Unlink').all():
            page.wait_for_selector("//*[text()='Unlink']")
            i.click()

def unlink(page):
    """unlink occasion"""
    try:
        for i in range(4):
            page.locator("//table//tr[1]//td[@class='cell action left']").click()
            page.wait_for_timeout(1200)
    except:
        pass




