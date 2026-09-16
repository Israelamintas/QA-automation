import pytest
from playwright.sync_api import expect

# def test_get_by_role(page, accept_cookies):
# page.goto("https://automationexercise.com/")
# accept_cookies()
# page.pause()
# page.get_by_role("link", name="Signup / Login").click()
# page.get_by_role("button", name="Login").click()
# page.goto("https://bootswatch.com/default/")
# page.pause()
# page.locator("#navbarColor01").get_by_role("button", name="Dropdown").click()


def test_get_by_text(page):
    page.goto("https://automationexercise.com/")
    page.pause()
    page.get_by_text("Full-Fledged practice website for").first.click()


def test_get_by_placeholder(page):
    page.goto("https://automationexercise.com/login")
    page.pause()
    page.get_by_placeholder("Name").fill("Teste")


def test_get_by_label(page):
    page.goto("https://bootswatch.com/default/")
    page.pause()
    page.get_by_label("Valid input", exact=True).fill("Teste")
    page.get_by_label("Recipient's username", exact=True).fill("Teste")


def test_get_by_title(page):
    page.goto("https://bootswatch.com/default/")
    page.pause()
    page.get_by_title("Source Title").nth(1).click()


def test_locator_css(page):
    page.goto("https://automationexercise.com/")
    page.pause()
    page.locator("#accordian .panel-title").first.click()


def test_locator_xpath(page):
    page.goto("https://automationexercise.com/login")
    page.pause()
    page.locator('//*[@id="form"]/div/div/div[1]/div/form/button').click()


def test_click(page):
    page.goto("https://automationexercise.com/")
    page.pause()
    page.get_by_role("link", name="Website for automation").click(button="right")
    page.get_by_role("link", name="Website for automation").click(
        position={"x": 10, "y": 10}
    )
    page.get_by_role("link", name="Website for automation").click(
        position={"x": 0, "y": 0}
    )
    page.get_by_role("link", name="(5) H&M").click(
        modifiers=["Ctrl"]
    )  # (Alt|Control|ControlOrMeta|Meta|Shift)


def test_fill(page):
    page.goto("https://automationexercise.com/login")
    page.pause()
    page.get_by_role("textbox", name="Name").fill("Jeferson", timeout=10000)
    page.locator("form").filter(has_text="Signup").get_by_placeholder(
        "Email Address"
    ).fill("teste@teste.com")
    page.get_by_role("button", name="Signup").click()


def test_check_uncheck(page):
    page.goto("https://bootswatch.com/default/")
    page.pause()
    page.get_by_role("checkbox", name="Default checkbox").check()
    page.get_by_role("checkbox", name="Default checkbox").uncheck()
    page.pause()


def test_select_option(page):
    page.goto("https://bootswatch.com/default/")
    page.pause()
    page.get_by_label("Example select").select_option("2")
    page.get_by_label("Example multiple select").select_option(["3", "5"])


def test_press(page):
    page.goto("https://bootswatch.com/default/")
    page.pause()
    page.get_by_role("textbox", name="Example textarea").fill("teste teste teste")
    page.get_by_role("textbox", name="Example textarea").press("Control+A")
    page.get_by_role("textbox", name="Example textarea").press("Control+C")
    page.get_by_placeholder("name@example.com").press("Control+V")


def test_type(page):
    page.goto("https://bootswatch.com/default/")
    page.pause()
    page.get_by_role("textbox", name="Example textarea").type(
        "Lorem Ipsum is simply dummy text of the printing and typesetting industry.",
        delay=150,
    )


def test_hover(page):
    page.goto("https://automationexercise.com")
    page.pause()
    page.locator(".single-products:visible").filter(
        has_text="Madame Top For Women"
    ).hover()
    page.locator(
        "div:nth-child(9) > .product-image-wrapper > .single-products > .product-overlay > .overlay-content > .btn"
    ).click()


def test_dblclick(page):
    page.goto("https://automationexercise.com/login")
    page.pause()
    page.locator(".login-form h2").dblclick()


from playwright.sync_api import expect


def test_expect(page):
    page.goto("https://automationexercise.com")
    page.pause()
    page.locator(".single-products:visible").filter(
        has_text="Madame Top For Women"
    ).hover()
    page.locator(
        "div:nth-child(9) > .product-image-wrapper > .single-products > .product-overlay > .overlay-content > .btn"
    ).click()
    expect(page.locator("#cartModal")).to_contain_text(
        "Your product has been added to cart.", timeout=10000
    )
    expect(page.get_by_role("button", name="Continue Shopping")).to_be_visible()
    expect(page.get_by_role("button", name="Continue Shopping")).to_be_enabled()
    page.get_by_role("button", name="Continue Shopping").click()
    expect(page.locator("#cartModal")).not_to_be_visible()
