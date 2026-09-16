from playwright.sync_api import expect

from .base_page import BasePage


class Carrinho(BasePage):
    def validar_carrinho(
        self,
        indice_produto="0",
        cabecalho_descricao_produto="",
        descricao_produto="",
        preco_produto="",
        preco_total_produto="",
    ):
        produto = self.page.locator("#cart_info_table tbody tr").nth(
            int(indice_produto)
        )
        expect(produto.locator(".cart_description h4")).to_have_text(
            cabecalho_descricao_produto
        )
        expect(produto.locator(".cart_description p")).to_have_text(descricao_produto)
        expect(produto.locator(".cart_price p")).to_have_text(preco_produto)
        expect(produto.locator(".cart_total_price")).to_have_text(preco_total_produto)
