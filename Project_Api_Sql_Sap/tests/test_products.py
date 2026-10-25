from clients.api_client import APIClient
from clients.sql_client import SQLClient
from helpers.po_helper import (
    create_test_product,
    create_test_supplier,
    generate_unique_name,
)


def test_create_product_success(api_client: APIClient, sql_client: SQLClient):
    """Testa a criação de um produto vinculado a um fornecedor e valida no SQLite."""
    # 1. Arrange: Cria fornecedor base
    supplier = create_test_supplier(api_client)
    supplier_id = supplier["id"]
    product_name = generate_unique_name("Teclado_Mecanico")

    # 2. Act: Cria produto via API
    product = create_test_product(
        api_client,
        supplier_id=supplier_id,
        name=product_name,
        unit_price=250.50,
        quantity_in_stock=25,
    )

    # 3. Assert: Validação na resposta HTTP
    assert "id" in product
    assert product["name"] == product_name
    assert product["unit_price"] == 250.50
    assert product["quantity_in_stock"] == 25
    assert product["supplier_id"] == supplier_id

    # 4. Assert: Validação direta no Banco de Dados (Caixa-Branca)
    db_row = sql_client.get_first_row(
        "SELECT id, name, unit_price, quantity_in_stock, supplier_id FROM products WHERE id = ?",
        (product["id"],),
    )
    assert db_row is not None
    assert db_row["name"] == product_name
    assert db_row["unit_price"] == 250.50
    assert db_row["quantity_in_stock"] == 25
    assert db_row["supplier_id"] == supplier_id


def test_create_product_duplicate_name_conflict(api_client: APIClient):
    """Garante que a regra UNIQUE impede dois produtos com o mesmo nome (409)."""
    supplier = create_test_supplier(api_client)
    product_name = generate_unique_name("Monitor_Dell")

    # Cria o 1º produto
    create_test_product(api_client, supplier_id=supplier["id"], name=product_name)

    # Tenta criar o 2º produto com o mesmo nome
    payload_duplicado = {
        "name": product_name,
        "unit_price": 899.00,
        "quantity_in_stock": 5,
        "supplier_id": supplier["id"],
    }
    response = api_client.post(
        "/api/v1/products", data=payload_duplicado, expected_status_code=409
    )
    error_body = response.json()
    assert "já existe" in error_body.get("detail", "").lower()


def test_create_product_with_nonexistent_supplier(api_client: APIClient):
    """Valida integridade relacional: não permite produto com fornecedor inexistente (404)."""
    payload = {
        "name": generate_unique_name("Produto_Orfao"),
        "unit_price": 50.00,
        "quantity_in_stock": 10,
        "supplier_id": 999999,
    }
    response = api_client.post(
        "/api/v1/products", data=payload, expected_status_code=404
    )
    error_body = response.json()
    assert "não existe" in error_body.get("detail", "").lower()


def test_get_product_stock(api_client: APIClient):
    """Testa a consulta dedicada do saldo de estoque do produto."""
    supplier = create_test_supplier(api_client)
    product = create_test_product(
        api_client,
        supplier_id=supplier["id"],
        quantity_in_stock=42,
    )
    product_id = product["id"]

    # Consulta a rota dedicada /stock
    response = api_client.get(
        f"/api/v1/products/{product_id}/stock", expected_status_code=200
    )
    stock_data = response.json()
    assert stock_data["product_id"] == product_id
    assert stock_data["quantity_in_stock"] == 42


def test_list_products_filtered_by_supplier(api_client: APIClient):
    """Valida o filtro da listagem de produtos por ID de fornecedor (?supplier_id=X)."""
    supplier_a = create_test_supplier(api_client)
    supplier_b = create_test_supplier(api_client)

    # Cria 2 produtos para o Fornecedor A e 1 para o Fornecedor B
    prod_a1 = create_test_product(api_client, supplier_id=supplier_a["id"])
    prod_a2 = create_test_product(api_client, supplier_id=supplier_a["id"])
    create_test_product(api_client, supplier_id=supplier_b["id"])

    # Faz a requisição filtrando pelo Fornecedor A
    supplier_id = supplier_a["id"]
    response = api_client.get(
        "/api/v1/products",
        params={"supplier_id": supplier_id},
        expected_status_code=200,
    )
    products_list = response.json()

    retrieved_ids = [p["id"] for p in products_list]
    assert prod_a1["id"] in retrieved_ids
    assert prod_a2["id"] in retrieved_ids
    for p in products_list:
        assert p["supplier_id"] == supplier_a["id"]

