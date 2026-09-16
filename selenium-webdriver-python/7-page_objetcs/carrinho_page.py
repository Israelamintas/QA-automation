import conftest
from base_page import Base_page
from selenium.webdriver.common.by import By


class CarrinhoPage(Base_page):
    def __init__(self):
        self.driver = conftest.driver
        self.item_inventory = (
            By.XPATH,
            "//*[@class='inventory_item_name' and text() = '{nome_item}']",
        )
        self.conituar_comprando = (By.ID, "continue-shopping")

    def verificar_item_no_carrinho_existe(self, nome_item):
        item = self.item_inventory[0], self.item_inventory[1].format(
            nome_item=nome_item
        )
        self.verificar_se_elemento_existe(item)

    def clicar_continuar_comprando(self):
        self.clicar(self.conituar_comprando)
