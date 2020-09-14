from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as selerr

# URL for D&D alignment test
url = "http://easydamus.com/alignmenttest.html"

# Make sure the Chrome window is launched as an app (without navigation buttons or address bar)
opts = Options()
opts.add_argument("--app=" + url)
driver = webdriver.Chrome(options = opts)
driver.get(url)
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
print("Your alignment is " + result.text)

# Close the window
driver.quit()