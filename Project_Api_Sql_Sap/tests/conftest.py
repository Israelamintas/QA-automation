import sys
from pathlib import Path

import pytest

# Garante que o diretório 'tests' está no caminho de busca de módulos do Python
TESTS_DIR = Path(__file__).resolve().parent
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from clients.api_client import APIClient
from clients.sql_client import SQLClient
from configs import BASE_URL, DATABASE_PATH


@pytest.fixture(scope="session")
def api_client() -> APIClient:
    """Fixture que fornece uma instância configurada do cliente HTTP da API."""
    return APIClient(base_url=BASE_URL)


@pytest.fixture(scope="session")
def sql_client() -> SQLClient:
    """Fixture que fornece uma instância do cliente de banco de dados SQLite."""
    return SQLClient(database_path=DATABASE_PATH)
