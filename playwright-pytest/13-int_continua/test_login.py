from cadastro_login import CadastroLogin
from playwright.sync_api import expect


def teste_login_valido(page):
    login = CadastroLogin(page)
    login.acessar_cadastro_login()
    login.fazer_login(email="teste@testeabcde.com", senha="123456789")
    expect(page.get_by_role("link", name="Logout")).to_be_visible()
    page.pause()
