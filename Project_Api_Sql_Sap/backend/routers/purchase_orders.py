import sqlite3
from typing import List, Optional

from db import get_connection
from fastapi import APIRouter, HTTPException, status
from models import PurchaseOrderCreate, PurchaseOrderResponse, StockMovementResponse

router = APIRouter(prefix="/api/v1/purchase-orders", tags=["Purchase Orders"])


# ==========================================
# 1. CRIAR ORDEM DE COMPRA (POST)
# ==========================================
@router.post(
    "",
    response_model=PurchaseOrderResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cria uma nova ordem de compra (nasce com status 'draft')",
)
def create_purchase_order(order_data: PurchaseOrderCreate):
    conn = get_connection()
    cursor = conn.cursor()

    # Validação 1: O fornecedor existe?
    cursor.execute(
        "SELECT id, active FROM suppliers WHERE id = ?", (order_data.supplier_id,)
    )
    supplier = cursor.fetchone()
    if not supplier:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fornecedor ID {order_data.supplier_id} não existe.",
        )

    # Validação 2: O produto existe?
    cursor.execute(
        "SELECT id, unit_price, supplier_id FROM products WHERE id = ?",
        (order_data.product_id,),
    )
    product = cursor.fetchone()
    if not product:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto ID {order_data.product_id} não existe.",
        )

    # Validação 3 (Regra SAP): O produto pertence mesmo a este fornecedor?
    if product["supplier_id"] != order_data.supplier_id:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"O produto ID {order_data.product_id} não pertence ao fornecedor ID {order_data.supplier_id}.",
        )

    # Cálculo automático do preço total
    unit_price = product["unit_price"]
    total_price = round(unit_price * order_data.quantity, 2)

    cursor.execute(
        """
        INSERT INTO purchase_orders (supplier_id, product_id, quantity, unit_price, total_price, status)
        VALUES (?, ?, ?, ?, ?, 'draft')
        """,
        (
            order_data.supplier_id,
            order_data.product_id,
            order_data.quantity,
            unit_price,
            total_price,
        ),
    )
    conn.commit()
    new_order_id = cursor.lastrowid

    cursor.execute("SELECT * FROM purchase_orders WHERE id = ?", (new_order_id,))
    created_order = cursor.fetchone()
    conn.close()

    return dict(created_order)


# ==========================================
# 2. LISTAR ORDENS DE COMPRA (GET)
# ==========================================
@router.get(
    "",
    response_model=List[PurchaseOrderResponse],
    status_code=status.HTTP_200_OK,
    summary="Lista ordens de compra (permite filtrar por status)",
)
def list_purchase_orders(status_filter: Optional[str] = None):
    conn = get_connection()
    cursor = conn.cursor()

    if status_filter:
        cursor.execute(
            "SELECT * FROM purchase_orders WHERE status = ? ORDER BY id DESC",
            (status_filter,),
        )
    else:
        cursor.execute("SELECT * FROM purchase_orders ORDER BY id DESC")

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# ==========================================
# 3. BUSCAR ORDEM POR ID (GET)
# ==========================================
@router.get(
    "/{order_id}",
    response_model=PurchaseOrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém detalhes de uma ordem de compra pelo ID",
)
def get_purchase_order(order_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM purchase_orders WHERE id = ?", (order_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ordem de compra ID {order_id} não foi encontrada.",
        )

    return dict(row)


# ==========================================
# 4. WORKFLOW: SUBMETER (draft -> pending_approval)
# ==========================================
@router.post(
    "/{order_id}/submit",
    response_model=PurchaseOrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Submete ordem para aprovação (draft -> pending_approval)",
)
def submit_purchase_order(order_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM purchase_orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()

    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="Ordem de compra não encontrada.")

    if order["status"] != "draft":
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Apenas ordens em status 'draft' podem ser submetidas. Status atual: '{order['status']}'.",
        )

    cursor.execute(
        "UPDATE purchase_orders SET status = 'pending_approval', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (order_id,),
    )
    conn.commit()

    cursor.execute("SELECT * FROM purchase_orders WHERE id = ?", (order_id,))
    updated_order = cursor.fetchone()
    conn.close()

    return dict(updated_order)


# ==========================================
# 5. WORKFLOW: APROVAR (pending_approval -> approved)
# ==========================================
@router.post(
    "/{order_id}/approve",
    response_model=PurchaseOrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Aprova a ordem de compra (pending_approval -> approved)",
)
def approve_purchase_order(order_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM purchase_orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()

    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="Ordem de compra não encontrada.")

    if order["status"] != "pending_approval":
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Apenas ordens 'pending_approval' podem ser aprovadas. Status atual: '{order['status']}'.",
        )

    cursor.execute(
        "UPDATE purchase_orders SET status = 'approved', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (order_id,),
    )
    conn.commit()

    cursor.execute("SELECT * FROM purchase_orders WHERE id = ?", (order_id,))
    updated_order = cursor.fetchone()
    conn.close()

    return dict(updated_order)


# ==========================================
# 6. WORKFLOW: RECEBER MERCADORIA (approved -> received + AUMENTA ESTOQUE)
# ==========================================
@router.post(
    "/{order_id}/receive",
    response_model=PurchaseOrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Recebe mercadoria no armazém (atualiza estoque físico e registra auditoria)",
)
def receive_purchase_order(order_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM purchase_orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()

    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="Ordem de compra não encontrada.")

    # REGRA CRÍTICA: Só recebe se já foi aprovada!
    if order["status"] != "approved":
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Não é possível receber mercadoria de ordem com status '{order['status']}'. A ordem precisa estar 'approved'.",
        )

    try:
        # Ação 1: Atualiza status da ordem para 'received'
        cursor.execute(
            "UPDATE purchase_orders SET status = 'received', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
            (order_id,),
        )

        # Ação 2: Incrementa o estoque físico do produto
        cursor.execute(
            "UPDATE products SET quantity_in_stock = quantity_in_stock + ? WHERE id = ?",
            (order["quantity"], order["product_id"]),
        )

        # Ação 3: Registra na tabela de auditoria stock_movements
        cursor.execute(
            """
            INSERT INTO stock_movements (product_id, movement_type, quantity, reference_order_id)
            VALUES (?, 'INBOUND', ?, ?)
            """,
            (order["product_id"], order["quantity"], order_id),
        )

        conn.commit()
    except Exception as e:
        conn.rollback()
        conn.close()
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar receção no banco: {str(e)}"
        )

    cursor.execute("SELECT * FROM purchase_orders WHERE id = ?", (order_id,))
    updated_order = cursor.fetchone()
    conn.close()

    return dict(updated_order)


# ==========================================
# 7. WORKFLOW: CANCELAR ORDEM
# ==========================================
@router.post(
    "/{order_id}/cancel",
    response_model=PurchaseOrderResponse,
    status_code=status.HTTP_200_OK,
    summary="Cancela a ordem de compra (se ainda não tiver sido recebida)",
)
def cancel_purchase_order(order_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM purchase_orders WHERE id = ?", (order_id,))
    order = cursor.fetchone()

    if not order:
        conn.close()
        raise HTTPException(status_code=404, detail="Ordem de compra não encontrada.")

    if order["status"] == "received":
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível cancelar uma ordem de compra que já foi fisicamente recebida no armazém.",
        )

    cursor.execute(
        "UPDATE purchase_orders SET status = 'cancelled', updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (order_id,),
    )
    conn.commit()

    cursor.execute("SELECT * FROM purchase_orders WHERE id = ?", (order_id,))
    updated_order = cursor.fetchone()
    conn.close()

    return dict(updated_order)
