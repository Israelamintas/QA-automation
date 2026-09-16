class BasePage:
    def __init__(self, page):
        self.page = page
        self.botao_home = page.get_by_role("link", name="Home")
        self.botao_produtos = page.get_by_role("link", name="Products")
        self.botao_carrinho = page.get_by_role("link", name="Cart")
        self.botao_cadastro_login = page.get_by_role("link", name="Signup / Login")

    def acessar_home(self):
        self.page.goto("https://automationexercise.com/")

    def acessar_carrinho(self):
        self.page.goto("https://automationexercise.com/view_cart")

    def acessar_cadastro_login(self):
        self.page.goto("https://automationexercise.com/login")
