from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import time

# URL for Enneagram type test
url = "https://www.eclecticenergies.com/enneagram/test-2"

# Make sure the Firefox window is launched headless
def headlessGram():
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.add_argument("--headless")
    driver = webdriver.Firefox(options=fireFoxOptions)
    driver.get(url)
    return driver

def gramScrape(driver):
    driver.find_element_by_class_name("button").click()
    time.sleep(0.5)
    lefts = driver.find_elements_by_class_name("l")
    rights = driver.find_elements_by_class_name("r")
    lefttext = []
    righttext = []
    for i in lefts:
        lefttext.append(i.text)
    for i in rights:
        righttext.append(i.text)
    arr = [lefttext, righttext]
    return arr


def gramSubmit(driver, arr):
    # You can probs reuse gramScrape()
    driver.find_element_by_class_name("button").click()
    time.sleep(0.5)
    lefts = driver.find_elements_by_class_name("l")
    for i in lefts:
        no = arr[0].index(i.text) # arr[0] is the array of names, arr[1] is the arr of vals
        print(str(no) + " - " + i.text + " - Value was " + str(arr[1][no]))
        btn = driver.find_element_by_css_selector("[name='q" + str(lefts.index(i)) + "'][value='"+str(arr[1][no])+"']")
        btn.click()
    btn = driver.find_element_by_css_selector("input[name='subm']")
    btn.click()
    final = driver.find_element_by_css_selector("a[title='link opens in new window']")
    return ("Your type is Type " + final.text[5])