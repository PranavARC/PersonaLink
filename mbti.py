from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# URL for MBTI personality test
url = "https://www.16personalities.com/free-personality-test"

# Make sure the Chrome window is launched as an app (without navigation buttons or address bar)
opts = Options()
opts.add_argument("--app=" + url)
driver = webdriver.Chrome(options = opts)
driver.get(url)

# Wait till the user is done taking the test, which will lead to the site URL changing
while(driver.current_url == url):
    pass

# Go to the results page once the survey is over
driver.get("https://www.16personalities.com/profile")

# If the user clicked on a random link while doing the survey, an error will occur, so catch it and exit
try:
    result = driver.find_elements_by_tag_name("td")[4]
    code = result.text
except IndexError:
    print("There was an issue, please try again")
else:
    print("Your type is: " + code)

# Close the window
driver.quit()