import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as selerr
URLS = ["https://www.16personalities.com/free-personality-test",
"http://easydamus.com/alignmenttest.html",
"https://www.truity.com/test/enneagram-personality-test"
]

def mbti(driver, url):
    while(driver.current_url == url):
        pass

    # Go to the results page once the survey is over
    driver.get("https://www.16personalities.com/profile")

    # If the user clicked on a random link while doing the survey, an error will occur
    # So go back to the survey page and try again
    try:
        result = driver.find_elements_by_tag_name("td")[4]
        code = result.text
    except IndexError:
        driver.get(url)
        return mbti(driver, url)
    else:
        return(code)

def dnd(driver, url):
    handles = []
    btn = driver.find_element_by_class_name("button")

    # Wait till the user finishes the survey and a pop-up window appears, making a second window handle
    while(True):
        handles = driver.window_handles
        if(len(handles) > 1):
            break
        if(driver.current_url != url):
            driver.get(url)

    # Switch to that window and extract the alignment
    driver.switch_to.window(handles[1])
    # An error will occur when closing the pop-up, so re-open it
    while(True):
        try:
            result = driver.find_elements_by_tag_name("b")[1]
        except selerr.NoSuchWindowException:
            driver.switch_to.window(driver.window_handles[0])
            btn.click()
            driver.switch_to.window(driver.window_handles[1])
        else:
            break
    return(result.text)

def enneagram(driver, url):
    # An RE of the results page (unique for each test)
    endurl = re.compile("https://www.truity.com/personality-test/[0-9]+/test-results/[0-9]+")

    # Until the user finishes the survey and until the survey page loads, wait
    while(True):
        # To deal with the user opening pop-ups
        handles = driver.window_handles
        if(len(handles) > 1):
            driver.switch_to.window(handles[1])
            try:
                driver.close()
            except selerr.NoSuchWindowException:
                pass
            driver.switch_to.window(handles[0])

        if(driver.current_url != url):
            if not(endurl.match(driver.current_url)):
                driver.get(url)
            elif(len(driver.find_elements_by_tag_name('h3')) > 0):
                break
    
    result = (driver.find_elements_by_tag_name('p')[4]).text
    begin = result.find("Your primary type is ") + len("Your primary type is ")
    end = result.find(".", begin)
    convert = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9}
    return convert[result[begin:end]]
    

def detect(site):
    # Make sure the Chrome window is launched as an app (without navigation buttons or address bar)
    opts = Options()
    opts.add_argument("--app=" + URLS[site])
    try:
        driver = webdriver.Chrome(options = opts)
        driver.get(URLS[site])
        if(site == 0):
            answer = mbti(driver, URLS[site])
        elif(site == 1):
            answer = dnd(driver, URLS[site])
        elif(site == 2):
            answer = enneagram(driver, URLS[site])
        driver.quit()
        return answer
    except:
        return("?") # ("Something went wrong, please try again")