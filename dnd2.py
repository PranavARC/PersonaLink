from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.request import urlopen
from webbrowser import open
import selenium.common.exceptions as selerr
import random
import time

# URL for MBTI personality test
url = "http://easydamus.com/alignmenttest.html"

# Make sure the Firefox window is launched headless
def headlessDND():
    fireFoxOptions = webdriver.FirefoxOptions()
    # fireFoxOptions.add_argument("--headless")
    driver = webdriver.Firefox(options=fireFoxOptions)
    driver.get(url)
    return driver

def dndScrape(driver):
    qsarr = []
    qs = driver.find_elements_by_class_name("question")
    opts = driver.find_elements_by_tag_name("p")
    trueopts = []
    for i in opts:
        first = i.text.find('\n\n')
        mainstr = i.text[first+2:]
        while(True):
            first = mainstr.find('\n')
            if(first == -1):
                trueopts.append(mainstr)
                break
            trueopts.append(mainstr[:first])
            mainstr = mainstr[first+1:]
    trueopts = trueopts[3:len(trueopts)-2]
    i = 0
    size = len(qs)
    for i in range(size):
        miniarr = []
        miniarr.append(qs[i].text)
        for j in range(4):
            miniarr.append((trueopts[4*i+j]))
        qsarr.append(miniarr)
    # for i in qsarr:
    #     for j in i:
    #         print(j)
    #     print("")
    return qsarr

def dndSubmit(driver, arr):
    i = 1
    size = len(arr)
    while(i <= size):
        if(arr[i-1]==0):
            i += 1
            continue
        namer = "q2" + "{0:0=2d}".format(i)
        rad = driver.find_element(By.CSS_SELECTOR,"[name='"+namer+"'][value='"+str(arr[i-1])+"']")
        rad.click()
        i += 1
    
    btn = driver.find_element_by_class_name("button")
    btn.click()
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    result = driver.find_elements_by_tag_name("b")[1]
    return("Your alignment is " + result.text)
        

    """
    qs = driver.find_elements_by_class_name("question")
    size = len(qs)
    start = 0
    while(start < size):
        choice = arr[qno]# random.randint(7)
        print(select[choice])
        btns = driver.find_elements(By.CSS_SELECTOR,"[data-index='" + str(choice) + "']")
        if(start == 0):
            driver.execute_script("window.scrollTo(0, 0)")
            btns[start].click()
            # webdriver.ActionChains(driver).move_to_element(btns[start]).click(btns[start]).perform()
            # doesn't work for Firefox
        else:
            btns[start].click()
        qno += 1
        start += 1
    if(page == 10):
        proceed = driver.find_element(By.CSS_SELECTOR,"[dusk='submit-button']")
    else:
        proceed = driver.find_element(By.CSS_SELECTOR,"[dusk='next-button']")
    proceed.click()
    if(page == 10):
        time.sleep(0.5)
    page += 1

time.sleep(0.5)
driver.get("https://www.16personalities.com/profile")
code = driver.find_elements_by_tag_name("td")[4].text
return("Your type is: " + code)

driver = headlessDND()
dndScrape(driver)
driver.quit()
"""