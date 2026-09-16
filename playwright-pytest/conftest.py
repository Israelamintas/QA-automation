import os
import shutil

import pytest


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args):
    return {
        **browser_type_launch_args,
        "args": [
            "--disable-features=Translate,TranslateUI",
            "--disable-translate",
            "--no-first-run",
            "--no-default-browser-check",
        ],
    }


@pytest.fixture(scope="function")
def context(browser):
    """Cria um novo contexto de navegador para cada teste, garantindo isolamento."""
    contexto = browser.new_context(
        base_url="https://automationexercise.com/",
        record_video_dir="videos",  # Salva vídeos dos testes
    )
    yield contexto
    contexto.close()


@pytest.fixture(scope="function")
def page(context):
    """Cria uma nova página por teste, com tempo de espera configurado."""
    pagina = context.new_page()
    pagina.set_default_timeout(10000)  # timeout padrão para ações
    pagina.set_default_navigation_timeout(30000)  # timeout para navegação
    yield pagina
    pagina.close()  # Opcional, pois o context fecha as pages também


STORAGE_FILE = "playwright/auth/state.json"


@pytest.fixture(scope="session")
def contexto(browser):
    if os.path.isfile(STORAGE_FILE):
        contexto = browser.new_context(
            base_url="https://automationexercise.com/",
            record_video_dir="videos",
            storage_state=STORAGE_FILE,
        )
    else:
        contexto = browser.new_context(
            base_url="https://automationexercise.com/", record_video_dir="videos"
        )

    yield contexto

    os.makedirs(os.path.dirname(STORAGE_FILE), exist_ok=True)

    if not os.path.isfile(STORAGE_FILE):
        contexto.storage_state(path=STORAGE_FILE)

    contexto.close()


@pytest.fixture
def accept_cookies(page):
    def _accept_cookies():
        consent_button = page.get_by_role("button", name="Consentir")
        if consent_button.count() and consent_button.first.is_visible():
            consent_button.first.click()

    return _accept_cookies
