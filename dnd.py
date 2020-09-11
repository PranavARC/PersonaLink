from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# URL for D&D alignment test
url = "http://easydamus.com/alignmenttest.html"

# Make sure the Chrome window is launched as an app (without navigation buttons or address bar)
opts = Options()
opts.add_argument("--app=" + url)
driver = webdriver.Chrome(options = opts)
driver.get(url)
handles = []

# Wait till the user finishes the survey and a pop-up window appears, making a second window handle
while(True):
    handles = driver.window_handles
    if(len(handles) > 1):
        break
    if(driver.current_url != url):
        driver.get(url)

# Switch to that window and extract the alignment
driver.switch_to.window(handles[1])
result = driver.find_elements_by_tag_name("b")[1]
align = result.text
print("Your alignment is: " + align)