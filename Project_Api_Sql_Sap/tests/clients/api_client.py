import logging
from typing import Any

import requests
from configs import BASE_URL

# Configura logs para podermos ver as chamadas no terminal se quisermos
logger = logging.getLogger(__name__)


class APIClient:
    """Cliente HTTP profissional que embrulha a biblioteca requests."""

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def build_url(self, endpoint: str) -> str:
        """Junta a URL base com o endpoint (ex: http://127.0.0.1:8000 + /api/v1/suppliers)."""
        return f"{self.base_url}{endpoint}"

    def verify_status_code(
        self, response: requests.Response, expected_status_code: int, url: str
    ):
        """O fiscal do teste: se o status for diferente do esperado, lança erro com detalhes."""
        assert response.status_code == expected_status_code, (
            f"Falha de status HTTP!\n"
            f"URL: {url}\n"
            f"Esperado: {expected_status_code}\n"
            f"Recebido: {response.status_code}\n"
            f"Resposta do Servidor: {response.text}"
        )

    def get(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        expected_status_code: int = 200,
    ) -> requests.Response:
        """Faz requisição GET e valida o código de status."""
        url = self.build_url(endpoint)
        response = requests.get(url, params=params, headers=self.headers)
        self.verify_status_code(response, expected_status_code, url)
        return response

    def get_json(
        self,
        endpoint: str,
        params: dict[str, Any] | None = None,
        expected_status_code: int = 200,
    ) -> dict | list:
        """Faz requisição GET, valida o status e já devolve o JSON convertido em dicionário/lista."""
        response = self.get(
            endpoint, params=params, expected_status_code=expected_status_code
        )
        return response.json()

    def post(
        self, endpoint: str, data: dict, expected_status_code: int = 201
    ) -> requests.Response:
        """Faz requisição POST (enviando JSON) e valida o código de status."""
        url = self.build_url(endpoint)
        response = requests.post(url, json=data, headers=self.headers)
        self.verify_status_code(response, expected_status_code, url)
        return response

    def post_json(
        self, endpoint: str, data: dict, expected_status_code: int = 201
    ) -> dict:
        """Faz requisição POST, valida o status e devolve o JSON da resposta."""
        response = self.post(
            endpoint, data=data, expected_status_code=expected_status_code
        )
        return response.json()
