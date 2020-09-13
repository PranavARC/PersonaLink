from selenium import webdriver
from selenium.webdriver.chrome.options import Options

URLS = ["https://www.16personalities.com/free-personality-test",
"http://easydamus.com/alignmenttest.html"
]

def mbti(driver, url):
    while(driver.current_url == url):
        pass

    # Go to the results page once the survey is over
    driver.get("https://www.16personalities.com/profile")

    # If the user clicked on a random link while doing the survey, an error will occur, so catch it and exit
    try:
        result = driver.find_elements_by_tag_name("td")[4]
        code = result.text
    except IndexError:
        return("Please don't click the hyperlinks, only do the quiz")
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
    print("pog")
    while(True):
        try:
            result = driver.find_elements_by_tag_name("b")[1]
        except:
            driver.switch_to.window(driver.window_handles[0])
            btn.click()
            driver.switch_to.window(driver.window_handles[1])
        else:
            break
    return(result.text)

def detect(site):
    # Make sure the Chrome window is launched as an app (without navigation buttons or address bar)
    opts = Options()
    opts.add_argument("--app=" + URLS[site])
    try:
        driver = webdriver.Chrome(options = opts)
        driver.get(URLS[site])
        if(site == 0):
            return mbti(driver, URLS[site])
        elif(site == 1):
            return dnd(driver, URLS[site])
    except:
        return("Something went wrong, please try again")
        
print(detect(0))