import sqlite3
from pathlib import Path
from typing import Any, Dict, List

from configs import DATABASE_PATH


class SQLClient:
    """Cliente para executar consultas e validações diretas no banco de dados SQLite."""

    def __init__(self, database_path: str = DATABASE_PATH):
        self.database_path = database_path

    def execute_query(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Executa uma consulta SQL (SELECT) e devolve as linhas como lista de dicionários.
        Exemplo: [{'id': 1, 'name': 'Altice', 'active': 1}]
        """
        db_file = Path(self.database_path)
        if not db_file.exists():
            raise FileNotFoundError(
                f"O arquivo do banco de dados não foi encontrado em: {self.database_path}"
            )

        # Abre a conexão com o banco
        connection = sqlite3.connect(self.database_path)

        # Faz com que cada linha venha com nomes de colunas acessíveis por chave
        connection.row_factory = sqlite3.Row
        cursor = connection.cursor()

        try:
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            # Converte as linhas do SQLite em dicionários padrão do Python
            return [dict(row) for row in rows]
        finally:
            cursor.close()
            connection.close()

    def get_first_row(self, sql: str, params: tuple = ()) -> Dict[str, Any] | None:
        """Atalho conveniente para quando esperamos apenas um único registo."""
        results = self.execute_query(sql, params)
        return results[0] if results else None
