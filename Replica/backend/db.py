import sqlite3
from pathlib import Path

# 1. Garante que o ficheiro do banco fica sempre dentro da pasta 'backend'
DB_PATH = Path(__file__).parent / "purchase_orders.db"


def get_connection():
    """Abre uma conexão com o banco SQLite e configura regras essenciais."""
    conn = sqlite3.connect(DB_PATH)

    # Faz o SQLite devolver linhas como dicionários (ex: row['name']) em vez de tuplas puras
    conn.row_factory = sqlite3.Row

    # OBRIGATÓRIO no SQLite: ativa a validação de chaves estrangeiras (Foreign Keys)
    conn.execute("PRAGMA foreign_keys = 1;")

    return conn


def init_db():
    """Cria as tabelas do sistema caso elas ainda não existam."""
    conn = get_connection()
    cursor = conn.cursor()
    # DDL: Data Definition Language (Comandos para estruturar as tabelas)
    cursor.executescript("""
        -- Tabela 1: Fornecedores
        CREATE TABLE IF NOT EXISTS suppliers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            contact_email TEXT NOT NULL,
            active INTEGER NOT NULL DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        -- Tabela 2: Produtos e Estoque Físico
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            unit_price REAL NOT NULL CHECK(unit_price > 0),
            quantity_in_stock INTEGER NOT NULL DEFAULT 0 CHECK(quantity_in_stock >= 0),
            supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        -- Tabela 3: Ordens de Compra (Purchase Orders)
        CREATE TABLE IF NOT EXISTS purchase_orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_id INTEGER NOT NULL REFERENCES suppliers(id),
            product_id INTEGER NOT NULL REFERENCES products(id),
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            unit_price REAL NOT NULL,
            total_price REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'draft' CHECK(
                status IN ('draft', 'pending_approval', 'approved', 'received', 'rejected', 'cancelled')
            ),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP
        );
        -- Tabela 4: Movimentações de Estoque (Auditoria idêntica ao SAP)
        CREATE TABLE IF NOT EXISTS stock_movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL REFERENCES products(id),
            movement_type TEXT NOT NULL CHECK(movement_type IN ('INBOUND', 'OUTBOUND')),
            quantity INTEGER NOT NULL,
            reference_order_id INTEGER REFERENCES purchase_orders(id),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()
    print("Base de dados e tabelas inicializadas com sucesso em:", DB_PATH)


# Se correr este arquivo diretamente (python db.py), ele cria o banco na hora!
if __name__ == "__main__":
    init_db()
