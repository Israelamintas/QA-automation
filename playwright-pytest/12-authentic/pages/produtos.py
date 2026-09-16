from .base_page import BasePage


class Produtos(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.botao_continuar_comprando = page.get_by_role(
            "button", name="Continue Shopping"
        )

    def adicionar_produto_ao_carrinho(self, indice_produto="0"):
        produto = self.page.locator(".product-overlay").nth(int(indice_produto))
        produto.get_by_role("button", name="Add to cart").click()
