from clients.api_client import APIClient
from clients.sql_client import SQLClient
from helpers.po_helper import create_test_supplier, generate_unique_name


def test_create_supplier_success(api_client: APIClient, sql_client: SQLClient):
    """Testa a criação de um fornecedor via API e valida a persistência direta no SQLite."""
    # 1. Arrange & Act (Criação via API)
    supplier_name = generate_unique_name("Supplier")
    response_data = create_test_supplier(api_client, name=supplier_name)

    # 2. Assert (Validação da resposta HTTP da API)
    assert "id" in response_data, "A resposta da API deve conter o campo 'id'"
    supplier_id = response_data["id"]
    assert response_data["name"] == supplier_name
    assert response_data["active"] is True

    # 3. Assert (Validação de Caixa-Branca diretamente no Banco SQLite)
    db_row = sql_client.get_first_row(
        "SELECT id, name, active FROM suppliers WHERE id = ?", (supplier_id,)
    )
    assert db_row is not None, "O fornecedor deve existir gravado no banco SQLite"
    assert db_row["name"] == supplier_name, "O nome gravado no banco deve ser idêntico"
    assert db_row["active"] == 1, "O fornecedor deve estar ativo (1) no banco"


def test_create_supplier_duplicate_name_conflict(api_client: APIClient):
    """Garante que a regra UNIQUE impede o cadastro de dois fornecedores com o mesmo nome (409)."""
    # 1. Cria o primeiro fornecedor com sucesso
    unique_name = generate_unique_name("UniqueCorp")
    create_test_supplier(api_client, name=unique_name)

    # 2. Tenta criar um segundo fornecedor com o mesmo nome
    payload_duplicado = {
        "name": unique_name,
        "contact_email": "outro_email@empresa.com",
        "active": True,
    }
    response = api_client.post(
        "/api/v1/suppliers", data=payload_duplicado, expected_status_code=409
    )

    # 3. Valida a mensagem de erro da API
    error_body = response.json()
    assert (
        "já existe" in error_body.get("detail", "").lower()
        or "already exists" in error_body.get("detail", "").lower()
    )


def test_get_supplier_by_id(api_client: APIClient):
    """Testa a busca de um fornecedor existente pelo seu ID."""
    novo_fornecedor = create_test_supplier(api_client)
    supplier_id = novo_fornecedor["id"]

    response = api_client.get(
        f"/api/v1/suppliers/{supplier_id}", expected_status_code=200
    )
    dados = response.json()
    assert dados["id"] == supplier_id
    assert dados["name"] == novo_fornecedor["name"]


def test_get_supplier_not_found(api_client: APIClient):
    """Testa a busca por um ID inexistente e valida o retorno 404 Not Found."""
    id_inexistente = 999999
    response = api_client.get(
        f"/api/v1/suppliers/{id_inexistente}", expected_status_code=404
    )
    error_body = response.json()
    assert "não foi encontrado" in error_body.get("detail", "").lower()
