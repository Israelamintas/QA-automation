import time

from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Edge()
browser.get("https://www.saucedemo.com/")

# find_element()
# username = browser.find_element(By.ID, "user-name")
# password = browser.find_element(By.ID, "password")

# sendo_keys
# username.send_keys("standard_user")
# password.send_keys("secret_sauce")

auth_fields = browser.find_elements(By.XPATH, "//*[@class='input_error form_input']")
print(auth_fields)
print(len(auth_fields))
assert len(auth_fields) == 2, "Não foram encontrados os campos de autenticação"
time.sleep(5)

browser.quit()
