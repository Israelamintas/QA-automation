from base_page import BasePage


class CadastroLogin(BasePage):

    def __init__(self, page):
        super().__init__(page)
        self.input_email_login = (
            page.locator("form")
            .filter(has_text="Login")
            .get_by_placeholder("Email Address")
        )
        self.input_senha_login = page.get_by_role("textbox", name="Password")
        self.botao_login = page.get_by_role("button", name="Login")

    def fazer_login(self, email="", senha=""):
        self.input_email_login.fill(email)
        self.input_senha_login.fill(senha)
        self.botao_login.click()
