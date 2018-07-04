from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import json
import math
import sys

url = sys.argv[1]
sector = sys.argv[2]

driver = webdriver.Firefox()
driver.get(url)

main_window = driver.current_window_handle

startAtLetter = sys.argv[3]
startAtFix = sys.argv[4]

numLettersInSector = driver.find_elements_by_xpath("//form/a")

for x in range(int(startAtLetter), len(numLettersInSector) + 1):
    # get the link to the next letter page
    letterPage = driver.find_element_by_xpath("//form/a[" + str(x) + "]")
    currentLetter = letterPage.get_attribute('innerHTML').replace('\n            ', '')
    print(currentLetter + str('lkfj'))

    letterPage.click()

    # get the number of fixes on this letter page
    numFixesInCurrentLetter = driver.find_elements_by_xpath("//table[@class='table table-condensed']//a")
    print("Length: " + str(len(numFixesInCurrentLetter)))

    # init the dictionary that will store the data for the fixes on this letter page
    fixesInCurrentLetter = dict()
    file = open(f'{sector}/{currentLetter}.txt', mode='a+')

    # iterate over the fixes on this letter page
    for i in range(int(startAtFix), len(numFixesInCurrentLetter)+1): # len(numFixesInCurrentLetter)

        if i % 5 == 0:
            column = 5
            row = i / 5
        else:
            column = i % 5
            row = math.floor(i / 5) + 1


        currentFix = driver.find_element_by_xpath(f'//table[@class="table table-condensed"]/tbody/tr[{row}]/td[{column}]/a')
        name = currentFix.get_attribute('innerHTML').replace('\n                        ', '')
        fixesInCurrentLetter[name] = dict()
        fixesInCurrentLetter[name]['name'] = name

        # open the fix page in a new tab

        driver.execute_script("arguments[0].scrollIntoView(false);", currentFix)
        webdriver.ActionChains(driver).key_down(Keys.COMMAND).click(currentFix).key_up(Keys.COMMAND).perform()

        # driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.TAB)

        # focus the new tab
        # webdriver.ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.TAB).key_up(Keys.TAB).key_up(Keys.CONTROL).perform()

        while len(driver.window_handles) < 2:
            sleep(1)
        driver.switch_to.window(driver.window_handles[1])

        # driver.switch_to_window(main_window)
        while len(driver.find_elements_by_xpath("//table[@class='table table-condensed']/tbody/tr[1]/td[2]")) < 1:
            sleep(1)

        latitude = driver.find_element_by_xpath("//table[@class='table table-condensed']/tbody/tr[1]/td[2]").get_attribute('innerHTML').replace('\n                ', '')
        longitude = driver.find_element_by_xpath("//table[@class='table table-condensed']/tbody/tr[2]/td[2]").get_attribute('innerHTML').replace('\n                ', '')
        state = driver.find_element_by_xpath("//table[@class='table table-condensed']/tbody/tr[4]/td[2]").get_attribute('innerHTML').replace('\n                ', '')
        artcc = driver.find_element_by_xpath("//table[@class='table table-condensed']/tbody/tr[5]/td[2]").get_attribute('innerHTML').replace('\n                ', '')
        type = driver.find_element_by_xpath("//table[@class='table table-condensed']/tbody/tr[6]/td[2]").get_attribute('innerHTML').replace('\n                ', '')
        updated = driver.find_element_by_xpath("//table[@class='table table-condensed']/tbody/tr[7]/td[2]").get_attribute('innerHTML').replace('\n                ', '')
        #
        # print(f'lat, long: {latitude}, {longitude}\nstate: {state}\nARTCC: {artcc}\ntype: {type}\nupdated: {updated}')
        print(fixesInCurrentLetter[name])
        file.write('\t{\n')
        file.write(f"\t\t'name': '{name}',\n")
        file.write(f"\t\t'latitude': '{latitude}',\n")
        file.write(f"\t\t'longitude': '{longitude}',\n")
        file.write(f"\t\t'state': '{state}',\n")
        file.write(f"\t\t'artcc': '{artcc}',\n")
        file.write(f"\t\t'type': '{type}',\n")
        file.write(f"\t\t'updated': '{updated}',\n")
        file.write('\t},\n')

        startAtFix = 1


        # close the tab for this fix
        # webdriver.ActionChains(driver).key_down(Keys.COMMAND).key_down('w').key_up('w').key_up(Keys.COMMAND).perform()
        driver.close()
        driver.switch_to_window(main_window)



    # json.dump(fixesInCurrentLetter, file, indent=2)

    driver.get(url)
