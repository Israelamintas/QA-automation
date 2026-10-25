from typing import Literal, Optional

from pydantic import BaseModel, Field

# ==========================================
# 1. MODELOS DE FORNECEDORES (Suppliers)
# ==========================================


class SupplierCreate(BaseModel):
    """Dados necessários para CRIAR um novo fornecedor."""

    name: str = Field(..., min_length=2, max_length=100, description="Nome da empresa")
    contact_email: str = Field(..., description="Email de contacto comercial")
    active: bool = Field(default=True, description="Se o fornecedor está ativo")


class SupplierResponse(SupplierCreate):
    """Dados devolvidos pela API ao CONSULTAR um fornecedor (inclui o ID gerado)."""

    id: int
    created_at: str


# ==========================================
# 2. MODELOS DE PRODUTOS (Products)
# ==========================================


class ProductCreate(BaseModel):
    """Dados necessários para CRIAR um novo produto."""

    name: str = Field(..., min_length=2, max_length=100, description="Nome do produto")
    unit_price: float = Field(..., gt=0, description="Preço unitário (deve ser > 0)")
    quantity_in_stock: int = Field(
        default=0, ge=0, description="Estoque físico inicial (>= 0)"
    )
    supplier_id: int = Field(..., gt=0, description="ID do fornecedor associado")


class ProductResponse(ProductCreate):
    """Dados devolvidos pela API ao CONSULTAR um produto."""

    id: int
    created_at: str


# ==========================================
# 3. MODELOS DE ORDENS DE COMPRA (Purchase Orders)
# ==========================================


class PurchaseOrderCreate(BaseModel):
    """
    Dados enviados pelo utilizador ao abrir uma nova compra.
    Repare: o utilizador NÃO envia o total_price nem o status!
    A nossa API vai calcular o total e definir o status como 'draft' automaticamente.
    """

    supplier_id: int = Field(..., gt=0, description="ID do fornecedor")
    product_id: int = Field(..., gt=0, description="ID do produto")
    quantity: int = Field(..., gt=0, description="Quantidade a comprar (deve ser > 0)")


class PurchaseOrderResponse(BaseModel):
    """Dados completos da Ordem de Compra devolvidos pela API."""

    id: int
    supplier_id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float
    status: Literal[
        "draft", "pending_approval", "approved", "received", "rejected", "cancelled"
    ]
    created_at: str
    updated_at: Optional[str] = None


# ==========================================
# 4. AUDITORIA DE ESTOQUE (Stock Movements)
# ==========================================


class StockMovementResponse(BaseModel):
    """Histórico de entradas e saídas de estoque."""

    id: int
    product_id: int
    movement_type: Literal["INBOUND", "OUTBOUND"]
    quantity: int
    reference_order_id: Optional[int] = None
    created_at: str
