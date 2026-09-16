import conftest
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class Base_page:
    def __init__(self):
        self.driver = conftest.driver

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def escrever(self, locator, texto):
        self.find_element(locator).send_keys(texto)

    def clicar(self, locator):
        self.find_element(locator).click()

    def verificar_se_elemento_existe(self, locator):
        assert self.find_element(
            locator
        ).is_displayed(), f"o elemento {locator} nao foi encontrado na tela"

    def pegar_texto(self, locator):
        self.esperar_elemento_aparecer(locator)
        return self.find_element(locator).text

    def esperar_elemento_aparecer(self, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(*locator))

    def verificar_elemento_existe(self, locator):
        assert self.find_element(
            locator
        ), f"o elemento {locator} nao foi encontrado na tela"

    def verificar_elemento_nao_existe(self, locator):
        assert (
            len(self.find_elements(locator)) == 0
        ), f"o elemento {locator} foi encontrado na tela"

    def click_duplo(self, locator):
        element = self.esperar_elemento_aparecer(locator)
        action = ActionChains(self.driver)
        action.double_click(element).perform()

    def click_direito(self, locator):
        element = self.esperar_elemento_aparecer(locator)
        action = ActionChains(self.driver)
        action.context_click(element).perform()

    def pressionar_tecla(self, locator, key):
        element = self.find_element(locator)
        if key == "ENTER":
            element.send_keys(Keys.ENTER)
        elif key == "ESPAÇO":
            element.send_keys(Keys.SPACE)
