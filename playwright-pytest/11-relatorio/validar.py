from base_page import BasePage
from playwright.sync_api import expect


def test_validar_home(page):
    pagina = BasePage(page)
    pagina.acessar_home()
    expect(page.get_by_role("heading", name="AutomationExercise")).to_be_visible()


def test_validar_produtos(page):
    pagina = BasePage(page)
    pagina.acessar_produtos()
    expect(page.get_by_role("img", name="Website for practice")).to_be_visible()


def test_validar_carrinho(page):
    pagina = BasePage(page)
    pagina.acessar_carrinho()
    expect(page.get_by_text("Home Shopping Cart")).to_be_visible()


def test_validar_login(page):
    pagina = BasePage(page)
    pagina.acessar_cadastro_login()
    expect(page.get_by_role("heading", name="Login to your account")).to_be_visible()


#### **Instalação**


# pip install pytest-xdist

### Exemplo – Execução paralela

# pytest -n 2

# pytest -n auto
# html#pytest .\validar.py --html=report.html
# é possivel criar um relatório html com o pytest, e criar docstreing ''' ''' e da um print nela no relatorio

"""
pytest --browser=firefox
pytest --browser-channel=chrome
pytest --slowmo 1000
pytest --device "iPhone 12"
pytest --tracing=on criar um video de como foi o teste
pytest --screenshot=only-on-failure salvar imagens do teste
"""
