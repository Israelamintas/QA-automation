"""
Utilitário para validação de dados em qualquer banco relacional.

Usa SQLAlchemy como camada única de conexão: o mesmo código funciona para
PostgreSQL, MySQL, Oracle, SQL Server e SQLite - muda apenas a connection string.
"""

import datetime
from decimal import Decimal
from pathlib import Path
from urllib.parse import quote_plus

from sqlalchemy import create_engine, text

# Raiz do projeto: a pasta acima de utilitarios/.
# Usada para resolver o caminho do SQLite independente de onde o script rodar.
RAIZ_PROJETO = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Conexão
# ---------------------------------------------------------------------------
def criar_engine(connection_string: str):
    """
    Cria uma engine do SQLAlchemy a partir de uma connection string.
    """
    return create_engine(connection_string)


def montar_connection_string(
    tipo_banco, usuario="", senha="", host="", porta="", database=""
):
    """
    Monta a connection string a partir do tipo de banco.
    Facilita a vida de quem não lembra o formato de cada dialeto.
    """
    tipo_banco = tipo_banco.lower()

    # Escapa caracteres especiais (@, :, /, #) em usuário e senha.
    # Sem isso, uma senha como 'p@ss:w0rd' quebra a connection string.
    usuario = quote_plus(str(usuario))
    senha = quote_plus(str(senha))

    if tipo_banco == "sqlite":
        caminho = Path(database)

        # Caminho relativo? Resolve a partir da raiz do projeto, e não do
        # diretório de onde o script foi executado.
        if not caminho.is_absolute():
            caminho = RAIZ_PROJETO / caminho

        # O SQLite cria um banco VAZIO se o arquivo não existir, o que gera o
        # erro confuso "no such table". Melhor falhar aqui, com mensagem clara.
        if not caminho.exists():
            raise FileNotFoundError(
                f"Banco SQLite nao encontrado: {caminho}\n"
                f"Rode o script de criacao do banco (criar_loja_db.py) antes dos testes."
            )

        return f"sqlite:///{caminho.as_posix()}"
    if tipo_banco in ("postgres", "postgresql"):
        return f"postgresql+psycopg2://{usuario}:{senha}@{host}:{porta}/{database}"
    if tipo_banco == "mysql":
        return f"mysql+pymysql://{usuario}:{senha}@{host}:{porta}/{database}"
    if tipo_banco == "oracle":
        return f"oracle+oracledb://{usuario}:{senha}@{host}:{porta}/?service_name={database}"
    if tipo_banco in ("sqlserver", "mssql"):
        return (
            f"mssql+pyodbc://{usuario}:{senha}@{host}:{porta}/{database}"
            f"?driver=ODBC+Driver+17+for+SQL+Server"
        )

    raise ValueError(f"Tipo de banco não suportado: {tipo_banco}")


# ---------------------------------------------------------------------------
# Execução de query
# ---------------------------------------------------------------------------
def normalizar_valor(valor):
    """
    Converte tipos que atrapalham a comparação em testes:
    Decimal -> float, datas -> texto ISO, bytes -> str.
    """
    if isinstance(valor, Decimal):
        return float(valor)
    if isinstance(valor, (datetime.date, datetime.datetime)):
        return valor.isoformat()
    if isinstance(valor, bytes):
        return valor.decode("utf-8", errors="ignore")
    return valor


def executar_query(engine, sql, parametros=None):
    """
    Executa uma query SELECT e retorna (colunas, linhas).
    As linhas já vêm normalizadas e prontas para comparação.

    parametros permite usar bind seguro (evita SQL injection):
        executar_query(engine, "SELECT * FROM usuarios WHERE email = :email",
                       {"email": "joao@teste.com"})
    """
    with engine.connect() as conexao:
        resultado = conexao.execute(text(sql), parametros or {})
        colunas = list(resultado.keys())
        linhas = [
            [normalizar_valor(valor) for valor in linha]
            for linha in resultado.fetchall()
        ]
    return colunas, linhas


# ---------------------------------------------------------------------------
# Validadores
# ---------------------------------------------------------------------------
def registro_existe(engine, sql, parametros=None):
    """Afirma que a query retorna ao menos 1 registro."""
    _, linhas = executar_query(engine, sql, parametros)
    assert len(linhas) > 0, (
        f"Esperava encontrar ao menos 1 registro, mas a query não retornou nada."
        f"\nSQL: {sql}"
    )
    print(f"OK - registro encontrado ({len(linhas)} linha(s)).")


def registro_nao_existe(engine, sql, parametros=None):
    """Afirma que a query NÃO retorna nenhum registro (ex: após exclusão)."""
    _, linhas = executar_query(engine, sql, parametros)
    assert len(linhas) == 0, (
        f"Esperava nenhum registro, mas a query retornou {len(linhas)} linha(s)."
        f"\nSQL: {sql}"
    )
    print("OK - nenhum registro encontrado, como esperado.")


def contar_registros(engine, sql, quantidade_esperada, parametros=None):
    """Valida a quantidade exata de linhas retornadas pela query."""
    _, linhas = executar_query(engine, sql, parametros)
    quantidade = len(linhas)
    assert quantidade == quantidade_esperada, (
        f"Esperava {quantidade_esperada} registro(s), mas encontrei {quantidade}."
        f"\nSQL: {sql}"
    )
    print(f"OK - {quantidade} registro(s), como esperado.")


def validar_valor_coluna(engine, sql, coluna, valor_esperado, parametros=None):
    """Valida o valor de uma coluna específica na primeira linha do resultado."""
    colunas, linhas = executar_query(engine, sql, parametros)

    assert len(linhas) > 0, f"A query não retornou nenhuma linha.\nSQL: {sql}"
    assert (
        coluna in colunas
    ), f"Coluna '{coluna}' não existe no resultado. Colunas: {colunas}"

    indice = colunas.index(coluna)
    valor_atual = linhas[0][indice]
    valor_esperado = normalizar_valor(valor_esperado)

    assert valor_atual == valor_esperado, (
        f"Valor da coluna '{coluna}' diferente do esperado."
        f"\nEsperado: {valor_esperado}"
        f"\nAtual:    {valor_atual}"
    )
    print(f"OK - coluna '{coluna}' = {valor_atual}, como esperado.")


def validar_resultado_esperado(engine, sql, resultado_esperado, parametros=None):
    """Compara o resultado completo da query com uma lista esperada."""
    _, linhas = executar_query(engine, sql, parametros)
    esperado = [
        [normalizar_valor(valor) for valor in linha] for linha in resultado_esperado
    ]
    assert linhas == esperado, (
        f"Resultado diferente do esperado."
        f"\nEsperado: {esperado}"
        f"\nAtual:    {linhas}"
    )
    print("OK - resultado igual ao esperado.")


# ---------------------------------------------------------------------------
# Debug / integração com o comparador de arquivos
# ---------------------------------------------------------------------------
def _formatar_tabela(colunas, linhas):
    dados = [colunas] + linhas
    larguras = [0] * len(colunas)
    for linha in dados:
        for idx, celula in enumerate(linha):
            larguras[idx] = max(larguras[idx], len(str(celula)))

    def formatar_linha(linha):
        return " | ".join(
            str(celula).ljust(larguras[idx]) for idx, celula in enumerate(linha)
        )

    separador = "-+-".join("-" * larguras[idx] for idx in range(len(colunas)))
    saida = [formatar_linha(colunas), separador]
    saida += [formatar_linha(linha) for linha in linhas]
    return "\n".join(saida)


def imprimir_resultado(engine, sql, parametros=None):
    """Imprime o resultado da query em formato de tabela (útil para debug)."""
    colunas, linhas = executar_query(engine, sql, parametros)
    print(_formatar_tabela(colunas, linhas))


def salvar_resultado_em_arquivo(engine, sql, caminho_arquivo, parametros=None):
    """
    Salva o resultado da query em um .txt formatado.
    Assim você pode reaproveitar o utilitário de comparação de arquivos:
    salvar o resultado atual e comparar com um arquivo base versionado no repo.
    """
    colunas, linhas = executar_query(engine, sql, parametros)
    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        f.write(_formatar_tabela(colunas, linhas) + "\n")
