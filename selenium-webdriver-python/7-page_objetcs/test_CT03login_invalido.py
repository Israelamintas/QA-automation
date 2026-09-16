import pytest
from base_page import Base_page
from home_page import HomePage
from login_page import LoginPage
from selenium.webdriver.common.by import By


@pytest.mark.usefixtures("setup_teardown")
class TestCT03:
    def test_ct03_login_invalido(self):
        mensagem_de_erro_esperada = (
            "Epic sadface: Username and password do not match any user in this service"
        )

        # instacia os objetos a serem usados no teste
        login_page = LoginPage()
        home_page = HomePage()
        # faz login usando o metodo da classe LoginPage
        login_page.fazer_login("standard_user", "secret_sauce")
        # login_page.fazer_login("standard_user", "zzzz")

        # verificar se o login falhou usando o metodo da classe HomePage
        login_page.verificar_login_falhou()

        # verifica o texto do erro usando o metodo da classe LoginPage
        login_page.verificar_texto_erro(mensagem_de_erro_esperada)
