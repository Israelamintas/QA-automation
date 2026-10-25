import sqlite3
from typing import List

from db import get_connection
from fastapi import APIRouter, HTTPException, status
from models import SupplierCreate, SupplierResponse

# 1. Cria o Router para agrupar todas as rotas de fornecedores
router = APIRouter(prefix="/api/v1/suppliers", tags=["Suppliers"])


# ==========================================
# ROTA 1: CRIAR NOVO FORNECEDOR (POST)
# ==========================================
@router.post(
    "",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo fornecedor",
)
def create_supplier(supplier_data: SupplierCreate):
    """
    Recebe os dados validados pelo Pydantic (SupplierCreate),
    guarda na base de dados SQLite e devolve o fornecedor com o ID criado.
    """
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO suppliers (name, contact_email, active)
            VALUES (?, ?, ?)
            """,
            (
                supplier_data.name,
                supplier_data.contact_email,
                int(supplier_data.active),
            ),
        )
        conn.commit()
        new_id = cursor.lastrowid  # Pega o ID que o SQLite acabou de gerar
    except sqlite3.IntegrityError:
        # Se tentar cadastrar um fornecedor com nome repetido (regra UNIQUE da tabela)
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Já existe um fornecedor cadastrado com o nome '{supplier_data.name}'.",
        )

    # Busca o registo recém-criado para devolver ao cliente
    cursor.execute("SELECT * FROM suppliers WHERE id = ?", (new_id,))
    created_supplier = cursor.fetchone()
    conn.close()

    return dict(created_supplier)


# ==========================================
# ROTA 2: LISTAR FORNECEDORES (GET)
# ==========================================
@router.get(
    "",
    response_model=List[SupplierResponse],
    status_code=status.HTTP_200_OK,
    summary="Lista todos os fornecedores cadastrados",
)
def list_suppliers(active_only: bool = False):
    """
    Lista todos os fornecedores.
    Permite filtrar apenas os ativos passando ?active_only=true na URL.
    """
    conn = get_connection()
    cursor = conn.cursor()

    if active_only:
        cursor.execute("SELECT * FROM suppliers WHERE active = 1 ORDER BY id ASC")
    else:
        cursor.execute("SELECT * FROM suppliers ORDER BY id ASC")

    rows = cursor.fetchall()
    conn.close()

    # Converte cada linha do SQLite em dicionário para o FastAPI gerar o JSON
    return [dict(row) for row in rows]


# ==========================================
# ROTA 3: BUSCAR FORNECEDOR POR ID (GET)
# ==========================================
@router.get(
    "/{supplier_id}",
    response_model=SupplierResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtém os detalhes de um fornecedor pelo ID",
)
def get_supplier(supplier_id: int):
    """
    Busca um fornecedor específico pelo seu ID.
    Se não existir, devolve erro 404 (Not Found).
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM suppliers WHERE id = ?", (supplier_id,))
    row = cursor.fetchone()
    conn.close()

    if not row:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Fornecedor com ID {supplier_id} não foi encontrado.",
        )

    return dict(row)
