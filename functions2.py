from selenium import webdriver
from selenium.webdriver.common.by import By
import time

URLS = [
    "https://www.16personalities.com/free-personality-test",
    "http://easydamus.com/alignmenttest.html",
    "https://www.eclecticenergies.com/enneagram/test-2"
]

# Open a headless browser for each case
def headless(site):
    fireFoxOptions = webdriver.FirefoxOptions()
    fireFoxOptions.add_argument("--headless")
    driver = webdriver.Firefox(options=fireFoxOptions)
    driver.get(URLS[site])
    return driver

def mbtiScrape(driver):
    arr = []
    qno = 1

    # Keep scraping each page till the next button is replaced by submit button 
    while(True):
        qs = driver.find_elements_by_class_name("statement")    # class containing the questions
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
    qNo = 0 # overall question number

    # Keep navigating pages until the result page is reached
    while(driver.current_url == URLS[0]):
        qs = driver.find_elements_by_class_name("question")
        size = len(qs)
        pgQNo = 0   # page question number

        # Answer every question on the page
        while(pgQNo < size):
            choice = arr[qNo]   # arr has the user answer for each question
            # Find every button of that value, and click the one corresponding to the question
            btns = driver.find_elements(By.CSS_SELECTOR,"[data-index='" + str(choice) + "']")
            if(pgQNo == 0):
                driver.execute_script("window.scrollTo(0, 0)")  # Scroll to top of page for first q
            btns[pgQNo].click()
            qNo += 1
            pgQNo += 1

        if(page == 10): # Last page, use submit button to see results
            proceed = driver.find_element(By.CSS_SELECTOR,"[dusk='submit-button']")
        else:
            proceed = driver.find_element(By.CSS_SELECTOR,"[dusk='next-button']")
        proceed.click()
        if(page == 10): # sleep before trying to scrape the answer to prevent errors
            time.sleep(0.5)
        page += 1

    time.sleep(0.5)
    driver.get("https://www.16personalities.com/profile")   # results page
    code = driver.find_elements_by_tag_name("td")[4].text
    return(code)

def dndScrape(driver):
    qsArr = []
    qs = driver.find_elements_by_class_name("question") # questions
    opts = driver.find_elements_by_tag_name("p")    # options (elements)
    trueOpts = []   # for the text of the options
    
    # Options text has new lines separating them and filler lines
    # Separate them into individual options
    for i in opts:
        first = i.text.find('\n\n')
        mainStr = i.text[first+2:]
        while(True):
            first = mainStr.find('\n')
            if(first == -1):
                trueOpts.append(mainStr)
                break
            trueOpts.append(mainStr[:first])
            mainStr = mainStr[first+1:]

    # Remove the filler lines
    trueOpts = trueOpts[3:len(trueOpts)-2]
    
    # Create an array of [question, opt1, opt2, opt3, opt4, question2, ...]
    i = 0
    size = len(qs)
    for i in range(size):
        miniArr = []
        miniArr.append(qs[i].text)
        for j in range(4):
            miniArr.append((trueOpts[4*i+j]))
        qsArr.append(miniArr)
    return qsArr

def dndSubmit(driver, arr):
    i = 0
    size = len(arr)

    while(i < size):
        if(arr[i] == 0):    # if radio buttons provided no value, skip
            i += 1
            continue
        namer = "q2" + "{0:0=2d}".format(i+1)   # names of questions: q201, q202, ...
        
        # Click the radio button of the corresponding question with the correct value
        rad = driver.find_element(By.CSS_SELECTOR,"[name='"+namer+"'][value='"+str(arr[i])+"']")
        rad.click()
        i += 1
    
    # Click the submit button, switch to the pop-up window, and scrape the result
    btn = driver.find_element_by_class_name("button")
    btn.click()
    handles = driver.window_handles
    driver.switch_to.window(handles[1])
    result = driver.find_elements_by_tag_name("b")[1]
    return(result.text)

def gramScrape(driver):
    # Click the button to enter the test, and wait for the page to load
    driver.find_element_by_class_name("button").click()
    time.sleep(0.5)

    # Scrape the left and right extremes of opinions
    lefts = driver.find_elements_by_class_name("l")
    rights = driver.find_elements_by_class_name("r")
    leftText = []
    rightText = []
    for i in lefts:
        leftText.append(i.text)
    for i in rights:
        rightText.append(i.text)

    # Return a 2D array of lefft and right extremes
    arr = [leftText, rightText]
    return arr

def gramSubmit(driver, arr):
    # Each time the page is opened, the questions relocate themselves
    # Reuse gramScrape and take the left extremes to search for the new positions of questions
    leftText = (gramScrape(driver))[0]

    for i in leftText:
        # Find the index where the value of the answer to our current question is stored
        no = arr[0].index(i) # arr[0] is the array of left extremes, arr[1] is the arr of vals
        btn = driver.find_element_by_css_selector("[name='q" + str(leftText.index(i)) + "'][value='"+str(arr[1][no])+"']")
        btn.click()
    
    # Click submit, scrape the type, and return
    btn = driver.find_element_by_css_selector("input[name='subm']")
    btn.click()
    final = driver.find_element_by_css_selector("a[title='link opens in new window']")
    return (final.text[5])