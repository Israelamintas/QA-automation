import time

from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Edge()
browser.get("https://demo.applitools.com/")
print(browser.title)

username = browser.find_element(By.ID, "username")
checkbox_remember_me = browser.find_element(By.XPATH, "//*[@type='checkbox']")

# is_displayed() - verifica se o elemento está visível na tela
print(username.is_displayed())
print(checkbox_remember_me.is_displayed())

# is_enabled() - verifica se o elemento está habilitado para interação
print(username.is_enabled())
print(checkbox_remember_me.is_enabled())

# is_selected() - verifica se o elemento está selecionado (checkbox, radio button)
print(checkbox_remember_me.is_selected())
assert checkbox_remember_me.is_selected() == False
assert not checkbox_remember_me.is_selected()

checkbox_remember_me.click()
print(checkbox_remember_me.is_selected())
browser.quit()
