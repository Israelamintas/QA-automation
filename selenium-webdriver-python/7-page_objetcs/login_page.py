import conftest
from base_page import Base_page
from selenium.webdriver.common.by import By


class LoginPage(Base_page):
    def __init__(self):
        self.driver = conftest.driver
        self.username_input = (By.ID, "user-name")
        self.password_input = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_message = (By.XPATH, "//*[@data-test='error']")

    def fazer_login(self, usuario, senha):
        self.escrever(self.username_input, usuario)
        self.escrever(self.password_input, senha)
        self.clicar(self.login_button)

    def verificar_login_falhou(self):
        self.verificar_se_elemento_existe(self.error_message)

    def verificar_texto_erro(self, texto_esperado):
        texto_atual = self.pegar_texto(self.error_message)
        assert (
            texto_atual == texto_esperado
        ), f"Erro: o texto atual '{texto_atual}' não corresponde ao texto esperado '{texto_esperado}'"
