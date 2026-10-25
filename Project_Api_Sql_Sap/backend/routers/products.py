import sqlite3
from typing import List, Optional

from db import get_connection
from fastapi import APIRouter, HTTPException, status
from models import ProductCreate, ProductResponse

# 1. Cria o Router para agrupar todas as rotas de produtos
router = APIRouter(prefix="/api/v1/products", tags=["Products"])


# ==========================================
# ROTA 1: CADASTRAR PRODUTO (POST)
# ==========================================
@router.post(
    "",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo produto associado a um fornecedor",
)
def create_product(product_data: ProductCreate):
    """
    Cadastra um produto.
    Valida se o fornecedor existe no banco antes de cadastrar.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # REGRA DE NEGÓCIO: O fornecedor existe?
    cursor.execute("SELECT id FROM suppliers WHERE id = ?", (product_data.supplier_id,))
    supplier = cursor.fetchone()
    if not supplier:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Não é possível cadastrar o produto: Fornecedor ID {product_data.supplier_id} não existe.",
        )

    try:
        cursor.execute(
            """
            INSERT INTO products (name, unit_price, quantity_in_stock, supplier_id)
            VALUES (?, ?, ?, ?)
            """,
            (
                product_data.name,
                product_data.unit_price,
                product_data.quantity_in_stock,
                product_data.supplier_id,
            ),
        )
        conn.commit()
        new_id = cursor.lastrowid
    except sqlite3.IntegrityError:
        # Se tentar cadastrar um produto com o mesmo nome de outro que já existe
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe um produto com o nome '{product_data.name}'.",
        )

    # Busca o produto criado para devolver ao cliente
    cursor.execute("SELECT * FROM products WHERE id = ?", (new_id,))
    created_product = cursor.fetchone()
    conn.close()

    return dict(created_product)


# ==========================================
# ROTA 2: LISTAR PRODUTOS (GET)
# ==========================================
@router.get(
    "",
    response_model=List[ProductResponse],
    status_code=status.HTTP_200_OK,
    summary="Lista todos os produtos (permite filtrar por fornecedor)",
)
def list_products(supplier_id: Optional[int] = None):
    """
    Lista todos os produtos.
    Se passar ?supplier_id=1, traz apenas os produtos daquele fornecedor.
    """
    conn = get_connection()
    cursor = conn.cursor()

    if supplier_id is not None:
        cursor.execute(
            "SELECT * FROM products WHERE supplier_id = ? ORDER BY id ASC",
            (supplier_id,),
        )
    else:
        cursor.execute("SELECT * FROM products ORDER BY id ASC")

    rows = cursor.fetchall()
    conn.close()

    return [dict(row) for row in rows]


# ==========================================
# ROTA 3: BUSCAR PRODUTO POR ID (GET)
# ==========================================
@router.get(
    "/{product_id}",
    response_model=ProductResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém detalhes de um produto pelo ID",
)
def get_product(product_id: int):
    """Busca um produto específico pelo ID."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {product_id} não foi encontrado.",
        )

    return dict(row)


# ==========================================
# ROTA 4: CONSULTAR ESTOQUE DO PRODUTO (GET)
# ==========================================
@router.get(
    "/{product_id}/stock",
    status_code=status.HTTP_200_OK,
    summary="Consulta o saldo de estoque atual do produto",
)
def get_product_stock(product_id: int):
    """Devolve apenas a quantidade física em estoque de um produto."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, quantity_in_stock FROM products WHERE id = ?", (product_id,)
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Produto com ID {product_id} não foi encontrado.",
        )

    return {
        "product_id": row["id"],
        "product_name": row["name"],
        "quantity_in_stock": row["quantity_in_stock"],
    }
