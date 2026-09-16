import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Edge()
browser.get("https://www.saucedemo.com/")

username = browser.find_element(By.ID, "user-name")
password = browser.find_element(By.ID, "password")
btn_login = browser.find_element(By.ID, "login-button")


# implicit wait - espera implícita
browser.implicitly_wait(5)

# explict wait - espera explícita
wait = WebDriverWait(browser, 10)

# expected_conditions - condições esperadas
# aparecer alerta na pagina
element = wait.until(EC.alert_is_present())
# aparecer texto, depois do click do botão
wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, "title"), "Products"))

# elemento ser clicável
wait.until(EC.element_to_be_clickable((By.ID, "login-button")))

# elemento ser visível
wait.until(EC.visibility_of_element_located((By.ID, "login-button")))

# elemento ser invisível
wait.until(EC.invisibility_of_element_located((By.ID, "login-button")))
# elemento ser hidden
# wait.until(EC.element_to_clickable(By.ID, "disabled-button"))
# elemento ser selecionado
# wait.until(EC.element_to_be_selected((By.ID, "login-button")))
browser.quit()
