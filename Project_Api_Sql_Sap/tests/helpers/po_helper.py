from typing import Optional
import uuid

from clients.api_client import APIClient


def generate_unique_name(prefix: str = "Item") -> str:
    """Gera um nome único usando UUID para evitar erros de nomes duplicados (UNIQUE)."""
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


def create_test_supplier(
    api_client: APIClient, name: Optional[str] = None, active: bool = True
) -> dict:
    """Cria um fornecedor de teste via API e devolve o JSON de resposta."""
    payload = {
        "name": name or generate_unique_name("Supplier"),
        "contact_email": f"contato_{uuid.uuid4().hex[:4]}@empresa.com",
        "active": active,
    }
    return api_client.post_json(
        "/api/v1/suppliers", data=payload, expected_status_code=201
    )


def create_test_product(
    api_client: APIClient,
    supplier_id: int,
    name: Optional[str] = None,
    unit_price: float = 100.0,
    quantity_in_stock: int = 10,
) -> dict:
    """Cria um produto de teste associado a um fornecedor existente."""
    payload = {
        "name": name or generate_unique_name("Product"),
        "unit_price": unit_price,
        "quantity_in_stock": quantity_in_stock,
        "supplier_id": supplier_id,
    }
    return api_client.post_json(
        "/api/v1/products", data=payload, expected_status_code=201
    )


def build_purchase_order_payload(
    supplier_id: int, product_id: int, quantity: int = 5
) -> dict:
    """Gera o payload básico para abrir uma ordem de compra."""
    return {"supplier_id": supplier_id, "product_id": product_id, "quantity": quantity}
