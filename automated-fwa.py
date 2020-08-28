from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

import datetime, calendar
import time
import sys
import os
import argparse
from dotenv import load_dotenv
load_dotenv()


USER = os.getenv('ess_user')
PASSWORD = os.getenv('ess_pass')
destinationLink = os.getenv('ess_link')
driver = webdriver.Chrome(ChromeDriverManager().install())
waitTime = 100
text = "Filing"
# driver = webdriver.Chrome(chromeLink)
#date format: mm/dd/yyyy
# destinationLink = "https://www.netflix.com/browse"
def init():
    driver.get(destinationLink)

def getWeekdaysOfMonth(year, month):
    weekends = [5, 6]
    num_days = calendar.monthrange(year, month)[1]
    days = [datetime.date(year,month, day) for day in range (1, num_days+1)]
    weekdays = [day.strftime("%m/%d/%Y") for day in days if (day.weekday() not in weekends)]
    return weekdays


def loginEss():
    password = driver.find_element_by_xpath("//input[@type='password']")
    user = driver.find_element_by_name('user')
    user.send_keys(USER)
    password.send_keys(PASSWORD + Keys.RETURN)


def fileFWA(date):
    try:
        element_present = EC.element_to_be_clickable(
            (By.ID, 'floatingbutton-1522'))
        WebDriverWait(driver, waitTime).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        businessTabAddBtn = driver.find_element_by_class_name("add")
        # businessTabAddBtn = driver.find_element_by_id("floatingbutton-1568")
        businessTabAddBtn.click()
        try:
            element_present2 = EC.element_to_be_clickable((By.NAME, 'date'))
            WebDriverWait(driver, waitTime).until(element_present2)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            businessDatePicker = driver.find_element_by_name("date")
            businessDatePicker.click()
            # businessDatePicker.send_keys("03/05/2020")
            businessDatePicker.send_keys(date)
            businessTimeIn = driver.find_element_by_name("time_in")
            businessTimeIn.click()
            businessTimeIn.send_keys("9:00 AM")
            businessTimeIn.send_keys(Keys.ENTER)
            businessTimeOut = driver.find_element_by_name("time_out")
            businessTimeOut.click()
            businessTimeOut.send_keys("6:00 PM")
            businessTimeOut.send_keys(Keys.ENTER)
            businessReason = driver.find_element_by_name("reason")
            businessReason.send_keys("FWA")
            save = driver.find_element_by_xpath(
                '//span[contains(text(), "Save")]')
            save.click()
            try:
                element_present2 = EC.element_to_be_clickable(
                    (By.XPATH, '//span[contains(text(), "Yes")]'))
                WebDriverWait(driver, waitTime).until(element_present2)
            except TimeoutException:
                print("Timed out waiting for page to load")
            finally:
                yes = driver.find_element_by_xpath(
                    '//span[contains(text(), "Yes")]')
                no = driver.find_element_by_xpath(
                    '//span[contains(text(), "No")]')
                no.click()
                time.sleep(1)
                return "success"

                # try:
                #     element_present2 = EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "OK")]'))
                #     WebDriverWait(driver, waitTime).until(element_present2)
                # except TimeoutException:
                #     print("Timed out waiting for page to load")
                # finally:
                #     ok = driver.find_element_by_xpath('//span[contains(text(), "OK")]')
                #     ok.click()
                #     time.sleep(5)




def initEss2():
    try:
        element_present = EC.element_to_be_clickable((By.ID, 'button-1017'))
        WebDriverWait(driver, waitTime).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        loginEss()
        try:
            element_present2 = EC.element_to_be_clickable(
                (By.ID, 'tab-1440-btnInnerEl'))
            WebDriverWait(driver, waitTime).until(element_present2)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            filingTab = driver.find_element_by_id("treeview-1038-record-337")
            actionChains = ActionChains(driver)
            actionChains.double_click(filingTab).perform()
            print(filingTab)
            businessTab = driver.find_element_by_id("treeview-1038-record-347")
            otTab = driver.find_element_by_id("treeview-1038-record-349")
            print(businessTab)
            actionChains = ActionChains(driver)
            actionChains.double_click(businessTab).perform()
            dateParams = sys.argv[1].split("/")
            dateType = len(dateParams)
            if (dateType == 2):
                # month
                # monthYear = sys.argv[1].split("/")
                monthYear = dateParams
                weekdays = getWeekdaysOfMonth(int(monthYear[1], 10), int(monthYear[0], 10))
                for i, date in enumerate(weekdays):
                    fileFWA(date)
                    print(date)
            elif (dateType == 3):
                # day
                for i, date in enumerate(sys.argv):
                    if (i == 0):
                        continue
                    fileFWA(date)
                    print(date)
            # if (sys.argv[1] == "month"):
            #     monthYear = sys.argv[2].split("/")
            #     weekdays = getWeekdaysOfMonth(int(monthYear[1], 10), int(monthYear[0], 10))
            #     for i, date in enumerate(weekdays):
            #         fileFWA(date)
            #         print(date)
            # else:
            #     for i, date in enumerate(sys.argv):
            #         if (i == 0):
            #             continue
            #         fileFWA(date)
            #         print(date)
            driver.close()


def initEss():
    try:
        element_present = EC.element_to_be_clickable((By.ID, 'button-1017'))
        WebDriverWait(driver, waitTime).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        loginEss()
        try:
            element_present2 = EC.element_to_be_clickable(
                (By.ID, 'tab-1440-btnInnerEl'))
            WebDriverWait(driver, waitTime).until(element_present2)
        except TimeoutException:
            print("Timed out waiting for page to load")
        finally:
            filingTab = driver.find_element_by_id("treeview-1038-record-337")
            actionChains = ActionChains(driver)
            actionChains.double_click(filingTab).perform()
            print(filingTab)
            businessTab = driver.find_element_by_id("treeview-1038-record-347")
            otTab = driver.find_element_by_id("treeview-1038-record-349")
            print(businessTab)
            actionChains = ActionChains(driver)
            actionChains.double_click(businessTab).perform()
            for i, date in enumerate(sys.argv):
                if (i == 0):
                    continue
                fileFWA(date)
                print(date)
            driver.close()


print(sys.argv)
parser = argparse.ArgumentParser(description='Automated filing of FWA in ESS.')
parser.add_argument('MM/DD/YYYY', metavar='MM/DD/YYYY', help='for individual date filing, provide "MM/DD/YYYY" (03/05/2020), for monthly weekdays date filing, provide "MM/YYYY" (03/2020)')
args = parser.parse_args()
try:
    init()
    initEss2()
except FileNotFoundError as err:
    print(f"Error: {err}")
    # set exit status to 1 to indicate error
    sys.exit(1)
