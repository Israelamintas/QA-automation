from clients.api_client import APIClient
from clients.sql_client import SQLClient
from helpers.po_helper import (
    build_purchase_order_payload,
    create_test_product,
    create_test_supplier,
)


def test_full_purchase_order_lifecycle_happy_path(
    api_client: APIClient, sql_client: SQLClient
):
    """Testa o ciclo completo SAP: draft -> pending_approval -> approved -> received.
    
    Valida a máquina de estados e comprova no SQLite:
    1. O incremento do saldo físico de estoque do produto.
    2. A criação do registo de auditoria em stock_movements (INBOUND).
    """
    # -------------------------------------------------------------
    # 1. SETUP DE DADOS BASE
    # -------------------------------------------------------------
    # Cria Fornecedor
    supplier = create_test_supplier(api_client)
    supplier_id = supplier["id"]

    # Cria Produto com estoque inicial = 10 unidades
    initial_stock = 10
    product = create_test_product(
        api_client,
        supplier_id=supplier_id,
        unit_price=100.0,
        quantity_in_stock=initial_stock,
    )
    product_id = product["id"]

    # -------------------------------------------------------------
    # 2. ETAPA 1: CRIAR ORDEM DE COMPRA (DRAFT)
    # -------------------------------------------------------------
    order_quantity = 5
    po_payload = build_purchase_order_payload(
        supplier_id=supplier_id, product_id=product_id, quantity=order_quantity
    )
    po = api_client.post_json(
        "/api/v1/purchase-orders", data=po_payload, expected_status_code=201
    )
    po_id = po["id"]

    assert po["status"] == "draft", "A ordem recém-criada deve nascer como 'draft'"
    assert po["total_price"] == 500.0  # 5 unidades * 100.0 de preço unitário

    # -------------------------------------------------------------
    # 3. ETAPA 2: SUBMETER PARA APROVAÇÃO (PENDING_APPROVAL)
    # -------------------------------------------------------------
    po_submitted = api_client.post_json(
        f"/api/v1/purchase-orders/{po_id}/submit", data={}, expected_status_code=200
    )
    assert po_submitted["status"] == "pending_approval"

    # -------------------------------------------------------------
    # 4. ETAPA 3: APROVAR A ORDEM (APPROVED)
    # -------------------------------------------------------------
    po_approved = api_client.post_json(
        f"/api/v1/purchase-orders/{po_id}/approve", data={}, expected_status_code=200
    )
    assert po_approved["status"] == "approved"

    # -------------------------------------------------------------
    # 5. ETAPA 4: RECEBER A CARGA NO ALMOXARIFADO (RECEIVED)
    # -------------------------------------------------------------
    po_received = api_client.post_json(
        f"/api/v1/purchase-orders/{po_id}/receive", data={}, expected_status_code=200
    )
    assert po_received["status"] == "received"

    # -------------------------------------------------------------
    # 6. VALIDAÇÃO DE CAIXA-BRANCA NO SQLITE (ESTOQUE E AUDITORIA)
    # -------------------------------------------------------------
    # A) O estoque aumentou de 10 para 15?
    product_row = sql_client.get_first_row(
        "SELECT quantity_in_stock FROM products WHERE id = ?", (product_id,)
    )
    assert product_row is not None
    expected_new_stock = initial_stock + order_quantity
    assert product_row["quantity_in_stock"] == expected_new_stock, (
        f"Estoque incorreto! Esperado {expected_new_stock}, mas obteve {product_row['quantity_in_stock']}"
    )

    # B) A linha de auditoria foi criada em stock_movements?
    movement_row = sql_client.get_first_row(
        "SELECT * FROM stock_movements WHERE reference_order_id = ?", (po_id,)
    )
    assert movement_row is not None, "Deve existir registro em stock_movements para a PO recebida"
    assert movement_row["product_id"] == product_id
    assert movement_row["movement_type"] == "INBOUND"
    assert movement_row["quantity"] == order_quantity


def test_cannot_receive_order_directly_from_draft(
    api_client: APIClient, sql_client: SQLClient
):
    """Regra de Negócio Crítica (SAP): Uma ordem em 'draft' NÃO pode ser recebida no armazém.
    
    Valida que a API rejeita com 400 e que o estoque físico não é alterado indevidamente.
    """
    # 1. Setup
    supplier = create_test_supplier(api_client)
    initial_stock = 20
    product = create_test_product(
        api_client, supplier_id=supplier["id"], quantity_in_stock=initial_stock
    )
    product_id = product["id"]

    # 2. Cria ordem (nasce em 'draft')
    po_payload = build_purchase_order_payload(
        supplier_id=supplier["id"], product_id=product_id, quantity=10
    )
    po = api_client.post_json(
        "/api/v1/purchase-orders", data=po_payload, expected_status_code=201
    )
    po_id = po["id"]

    # 3. Tentativa ilegal: Chamar /receive direto em 'draft'
    response = api_client.post(
        f"/api/v1/purchase-orders/{po_id}/receive", data={}, expected_status_code=400
    )
    error_body = response.json()
    assert "approved" in error_body.get("detail", "").lower()

    # 4. Validação no Banco: O estoque DEVE continuar exatamente 20!
    product_row = sql_client.get_first_row(
        "SELECT quantity_in_stock FROM products WHERE id = ?", (product_id,)
    )
    assert product_row["quantity_in_stock"] == initial_stock, "Estoque não deveria ter mudado!"

    # 5. Validação no Banco: NENHUMA movimentação deve ter sido gravada
    movement_row = sql_client.get_first_row(
        "SELECT * FROM stock_movements WHERE reference_order_id = ?", (po_id,)
    )
    assert movement_row is None, "Não deve haver movimentação para ordem não recebida"


def test_cannot_approve_order_without_submitting(api_client: APIClient):
    """Regra de Transição: Não é permitido aprovar uma ordem sem antes submetê-la (draft -> approved é proibido)."""
    supplier = create_test_supplier(api_client)
    product = create_test_product(api_client, supplier_id=supplier["id"])
    po = api_client.post_json(
        "/api/v1/purchase-orders",
        data=build_purchase_order_payload(supplier["id"], product["id"], 5),
        expected_status_code=201,
    )

    # Tenta aprovar diretamente do status draft
    response = api_client.post(
        f"/api/v1/purchase-orders/{po['id']}/approve", data={}, expected_status_code=400
    )
    error_body = response.json()
    assert "pending_approval" in error_body.get("detail", "").lower()


def test_cannot_cancel_already_received_order(api_client: APIClient):
    """Regra de Auditoria Fiscal: Mercadoria já recebida fisicamente no armazém NÃO pode ser cancelada."""
    # 1. Cria e leva até 'received'
    supplier = create_test_supplier(api_client)
    product = create_test_product(api_client, supplier_id=supplier["id"])
    po = api_client.post_json(
        "/api/v1/purchase-orders",
        data=build_purchase_order_payload(supplier["id"], product["id"], 2),
        expected_status_code=201,
    )
    po_id = po["id"]
    api_client.post(f"/api/v1/purchase-orders/{po_id}/submit", data={}, expected_status_code=200)
    api_client.post(f"/api/v1/purchase-orders/{po_id}/approve", data={}, expected_status_code=200)
    api_client.post(f"/api/v1/purchase-orders/{po_id}/receive", data={}, expected_status_code=200)

    # 2. Tenta cancelar a ordem que já foi recebida
    response = api_client.post(
        f"/api/v1/purchase-orders/{po_id}/cancel", data={}, expected_status_code=400
    )
    error_body = response.json()
    assert "já foi fisicamente recebida" in error_body.get("detail", "").lower()

