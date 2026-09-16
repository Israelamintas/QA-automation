import time

from selenium import webdriver

browser = webdriver.Edge()
browser.get("https://leogcarvalho.github.io/test-automation-practice")
print(browser.title)

# current_url = browser.current_url
print(browser.current_url)
# page_source = browser.page_source
print(browser.page_source)
browser.quit()
