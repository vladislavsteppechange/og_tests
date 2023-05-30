from playwright.sync_api import expect
import csv


def validate_data (selector):
    assert type(selector.all()) is list
    assert len(selector.all()) > 0


"""OG - 28"""
def validate_review_table(page, table_names):
    """validate Review table"""
    expect(page.locator("//*[@class='p-datatable-table']")).to_be_visible()
    elems = page.locator("//*[@class='p-column-title']")

    j = 0
    for i in elems.all():
        assert i.inner_text() == table_names[j]
        j += 1


def validate_priority(elems_of_priority, list_of_priority):
    count = 0
    for i in elems_of_priority.all():
        assert i.inner_text() == list_of_priority[count]
        count += 1


def validate_reach_reneview_table(elems, flag):
    value_of_elems_reach = []
    for i in elems:
        value_of_elems_reach.append(int(i.inner_text().replace(',','')))
    if flag == 0:
        assert value_of_elems_reach[0]<value_of_elems_reach[1]
        assert value_of_elems_reach[1]<value_of_elems_reach[2]
        assert value_of_elems_reach[2]<value_of_elems_reach[3]
    else:
        assert value_of_elems_reach[0] > value_of_elems_reach[1]
        assert value_of_elems_reach[1] > value_of_elems_reach[2]
        assert value_of_elems_reach[2] > value_of_elems_reach[3]


def validate_reach_reneview_table_for_few_sections(elems, flag):
    value_of_elems_reach = []
    for i in elems:
        value_of_elems_reach.append(int(i.inner_text().replace(',','')))
    if flag == 0:
        assert value_of_elems_reach[0] < value_of_elems_reach[1]
        assert value_of_elems_reach[1] > value_of_elems_reach[2]
        assert value_of_elems_reach[2] < value_of_elems_reach[3]
    else:
        assert value_of_elems_reach[0] > value_of_elems_reach[1]
        assert value_of_elems_reach[1] < value_of_elems_reach[2]
        assert value_of_elems_reach[2] > value_of_elems_reach[3]


def validate_csv(flag):
    some = []
    with open('./utils/csv/test_omm.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            some.append(', '.join(row))

    assert some[0].split(',')[0] == '"Campaign Name"'
    assert some[3].split(',')[0] == '"Media Property ID"'
    assert some[5].split(',')[0] == '"Section Name"'
    if flag == 0:
        assert some[6].split(',')[0] == '"About"'
        assert some[8].split(',')[0] == '"Jogging"'
    else:
        assert len(some) < 7


"""OG-42"""
def validate_ex_default_state(page, SPRITE, US):
    """validate default value brands"""
    assert page.locator("//section[@class='strategy-selection']//*[@class='p-multiselect p-component p-inputwrapper p-multiselect-chip p-inputwrapper-filled']").inner_text() == SPRITE
    """validate default value markets"""
    assert page.locator("//section[@class='strategy-selection']//*[@class='p-treeselect-label']").inner_text() == US
    """validate buttons and sections"""
    expect(page.locator("//*[@class='explore-occasion__footer-buttons strategy-selection__footer-buttons']//button[1]")).to_be_enabled()
    expect(page.locator("//*[@class='explore-occasion__footer-buttons strategy-selection__footer-buttons']//button[2]")).to_be_enabled()
    expect(page.locator("//*[@class='select__title'][text()='Occasion Type']/following::div[@class='p-multiselect-label'][1]")).not_to_be_visible()
    expect(page.locator("//div[@class='media__container grid-container__item']")).not_to_be_visible()