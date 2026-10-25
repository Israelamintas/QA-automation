import os
from pathlib import Path

# ========================================================
# 1. URL BASE DA API
# ========================================================
# Se o sistema tiver uma variável de ambiente BASE_URL definida, usa-a.
# Se não tiver, assume por padrão o nosso servidor local Uvicorn na porta 8000.
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


# ========================================================
# 2. CAMINHO DINÂMICO PARA A BASE DE DADOS SQLITE
# ========================================================
# Calcula o caminho exato até à pasta backend/purchase_orders.db
# independentemente de onde você rodar o comando no terminal!
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = PROJECT_ROOT / "backend" / "purchase_orders.db"

DATABASE_PATH = os.getenv("DATABASE_PATH", str(DEFAULT_DB_PATH))
