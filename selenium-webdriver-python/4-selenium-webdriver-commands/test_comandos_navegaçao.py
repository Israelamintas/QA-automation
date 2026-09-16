import time

from selenium import webdriver

browser = webdriver.Chrome()
browser.get("https://leogcarvalho.github.io/test-automation-practice")
browser.get("https://www.google.com")
time.sleep(5)
browser.quit()
