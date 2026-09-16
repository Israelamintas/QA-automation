import conftest


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
        return self.find_element(locator).text
