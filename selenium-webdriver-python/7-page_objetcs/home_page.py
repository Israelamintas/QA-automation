import conftest
from base_page import Base_page
from selenium.webdriver.common.by import By


class HomePage(Base_page):
    def __init__(self):
        self.driver = conftest.driver
        self.title = (By.XPATH, "//span[@class='title']")
        self.item_inventory = (
            By.XPATH,
            "//*[@class='inventory_item_name ' and text() = '{nome_item}']",
        )
        # adicioinando o produto ao carrinho e validando se o mesmo foi adicionado
        self.botao_adicionar_carrinho = (By.XPATH, "//*[text()='Add to cart']")
        self.icone_carrinho = (By.XPATH, "//*[@class='shopping_cart_link']")

    def verificar_login_sucesso(self):
        self.verificar_se_elemento_existe(self.title)

    def adicionar_item_ao_carrinho(self, nome_item):
        item = self.item_inventory[0], self.item_inventory[1].format(
            nome_item=nome_item
        )
        self.clicar(item)
        self.clicar(self.botao_adicionar_carrinho)

    def acessar_carrinho(self):
        self.clicar(self.icone_carrinho)
