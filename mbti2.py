from selenium import webdriver
# from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# import random
import time

# URL for MBTI personality test
url = "https://www.16personalities.com/free-personality-test"

# For debug purposes
select = {
    0 : "option agree max",
    1 : "option agree med",
    2 : "option agree min",
    3 : "option neutral",
    4 : "option disagree min",
    5 : "option disagree med",
    6 : "option disagree max"
}

# Make sure the Firefox window is launched headless
def headlessMbti():
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.add_argument("--headless")
    driver = webdriver.Firefox(options=fireFoxOptions)
    driver.get(url)
    return driver

def mbtiScrape(driver):
    arr = []
    qno = 1
    while(True):   # Keep scraping till the next button is replaced by submit button 
        qs = driver.find_elements_by_class_name("statement")
        for i in qs:
            arr.append(str(qno) + ". " + i.text)    # [question #]. [question] 
            qno += 1
        proceed = driver.find_elements(By.CSS_SELECTOR,"[dusk='next-button']")
        if(len(proceed) == 0):
            break   # No next button found, so last page reached
        proceed[0].click()
    return arr

def mbtiSubmit(driver, arr):
    page = 1
    qno = 0
    while(driver.current_url == url):
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

# driver = headlessmbti()
# for i in mbtiscrape(driver):
#     print(i)
# driver.get(url) 
# print(mbticheck(driver))
# driver.quit()