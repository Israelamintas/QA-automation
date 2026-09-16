import time

import conftest
import pytest
from home_page import HomePage
from login_page import LoginPage


@pytest.mark.usefixtures("setup_teardown")
class TestCT02:
    def test_ct02_login_valido(self):
        # instacia os objetos a serem usados no teste
        login_page = LoginPage()
        home_page = HomePage()
        # faz login usando o metodo da classe LoginPage
        login_page.fazer_login("standard_user", "secret_sauce")
        # verifica se o login foi bem sucedido usando o metodo da classe HomePage
        home_page.verificar_login_sucesso()
