import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# URL for Enneagram test, and results page
url = "https://www.truity.com/test/enneagram-personality-test"
endurl = re.compile("https://www.truity.com/personality-test/[0-9]+/test-results/[0-9]+")

# Make sure the Chrome window is launched as an app (without navigation buttons or address bar)
opts = Options()
opts.add_argument("--app=" + url)
driver = webdriver.Chrome(options = opts)
driver.get(url)

while(True):
    # To deal with the user opening pop-ups
    handles = driver.window_handles
    if(len(handles) > 1):
        driver.switch_to.window(handles[1])
        driver.close()
        driver.switch_to.window(handles[0])

    if(driver.current_url != url):
        if not(endurl.match(driver.current_url)):
            driver.get(url)
        elif(len(driver.find_elements_by_tag_name('h3')) > 0):
            break

result = (driver.find_elements_by_tag_name('p')[4]).text
begin = result.find("Your primary type is ") + len("Your primary type is ")
end = result.find(".", begin)
print("Type " + result[begin:end])
driver.quit()