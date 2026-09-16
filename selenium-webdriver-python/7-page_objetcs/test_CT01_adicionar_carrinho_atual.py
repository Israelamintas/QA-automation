import pytest
from carrinho_page import CarrinhoPage
from home_page import HomePage
from login_page import LoginPage


@pytest.mark.usefixtures("setup_teardown")
class TestCT01:
    def test_ct01_adicionar_carrinho(self):
        login_page = LoginPage()
        home_page = HomePage()
        carrinho_page = CarrinhoPage()
        # faz login usando o metodo da classe LoginPage
        login_page.fazer_login("standard_user", "secret_sauce")
        home_page.adicionar_item_ao_carrinho("Sauce Labs Backpack")

        home_page.acessar_carrinho()
        carrinho_page.verificar_item_no_carrinho_existe("Sauce Labs Backpack")

        # clica no botão continuar comprando
        carrinho_page.clicar_continuar_comprando()

        home_page.adicionar_item_ao_carrinho("Sauce Labs Bolt T-Shirt")

        home_page.acessar_carrinho()
        carrinho_page.verificar_item_no_carrinho_existe("Sauce Labs Bolt T-Shirt")
