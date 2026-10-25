from db import init_db
from fastapi import FastAPI
from routers import (  # <-- 1. Importa purchase_orders
    products,
    purchase_orders,
    suppliers,
)

init_db()

app = FastAPI(
    title="Purchase Order & Stock Management API",
    version="1.0.0",
    description="API empresarial de Gestão de Compras e Estoque (Inspirada em fluxos SAP).",
)

# Conecta todos os routers
app.include_router(suppliers.router)
app.include_router(products.router)
app.include_router(purchase_orders.router)  # <-- 2. Conecta as ordens de compra


@app.get("/", tags=["Health"])
def root():
    return {
        "message": "Purchase Order API está online e pronta para receber pedidos!",
        "docs_url": "/docs",
    }
