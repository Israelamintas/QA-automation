from cadastro_login import CadastroLogin
from playwright.sync_api import expect


def test_login_invalido(page):
    login = CadastroLogin(page)
    login.acessar_cadastro_login()
    login.fazer_login(email=" teste@testeabcde.com", senha="123456789")
    expect(page.get_by_text("Your email or password is incorrect.")).to_be_visible()
    expect(page.get_by_role("link", name="Login")).to_be_visible()


def teste_login_valido(page):
    login = CadastroLogin(page)
    login.acessar_cadastro_login()
    login.fazer_login(email="teste@testeabcde.com", senha="123456789")
    expect(page.get_by_role("link", name="Logout")).to_be_visible()
    page.pause()


def test_usuario_nao_logado(page):
    login = CadastroLogin(page)
    login.acessar_cadastro_login()
    expect(page.get_by_role("link", name="Logout")).to_be_invisible()
    page.pause()


def test_logout(page):
    login = CadastroLogin(page)
    login.acessar_cadastro_login()
    login.botao_logout.click()
    expect(page.get_by_role("link", name="Login")).to_be_visible()
