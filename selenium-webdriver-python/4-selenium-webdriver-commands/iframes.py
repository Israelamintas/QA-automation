import time

from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Edge()
browser.get("https://leogcarvalho.github.io/test-automation-practice/")


# # Mudar o foco para dentro do iframe
# driver.switch_to.frame("nome_ou_id_do_iframe")

# # Ou por índice (0, 1, 2... se houver vários iframes)
# driver.switch_to.frame(0)

# # Ou passando o elemento WebElement do iframe
# iframe_element = driver.find_element(By.ID, "meu_iframe")
# driver.switch_to.frame(iframe_element)

# # Agora sim, pode interagir com o que está dentro
# driver.find_element(By.ID, "campo_dentro_do_iframe").send_keys("texto")

# # Depois de terminar, volta pro contexto principal
# driver.switch_to.default_content()

# sempre respeitar a hierarquia do iframe, se tiver um iframe dentro de outro,
#  tem que ir para o primeiro e depois para o segundo
browser.quit()
