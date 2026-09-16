import os
import re
import tempfile
from typing import Optional

import pandas as pd
import PyPDF2
from openpyxl import load_workbook


def comparar_arquivos(
    arquivo_base,
    arquivo_atual,
    linhas_ignorar=None,
    padrao_ignorar="",
    bytes_ignorar=0,
    encoding="utf-8",
):
    """
    Compara dois arquivos de texto linha por linha.
    """

    if linhas_ignorar is None:
        linhas_ignorar = []

    with open(arquivo_base, "r", encoding=encoding) as f1, open(
        arquivo_atual, "r", encoding=encoding
    ) as f2:
        linhas_arquivo1 = f1.readlines()
        linhas_arquivo2 = f2.readlines()

    tem_diferenca = False
    bytes_diferenca = 0

    for i, (linha1, linha2) in enumerate(zip(linhas_arquivo1, linhas_arquivo2)):

        if (i + 1) in linhas_ignorar:
            continue

        if padrao_ignorar:
            linha1 = re.sub(padrao_ignorar, "", linha1, flags=re.DOTALL)
            linha2 = re.sub(padrao_ignorar, "", linha2, flags=re.DOTALL)

        if linha1 != linha2:
            print(f"Diferença na linha{i + 1}:")
            print(f"Arquivo Base:{linha1.strip()}")
            print(f"Arquivo Atual:{linha2.strip()}")

            bytes_linha1 = linha1.encode()
            bytes_linha2 = linha2.encode()

            max_len = max(len(bytes_linha1), len(bytes_linha2))

            for j in range(max_len):
                try:
                    if bytes_linha1[j] != bytes_linha2[j]:
                        bytes_diferenca += 1
                except IndexError:
                    bytes_diferenca += 1

            if bytes_diferenca > bytes_ignorar or bytes_ignorar == 0:
                tem_diferenca = True

    assert len(linhas_arquivo2) > 0, "Arquivo atual está em branco, verifique!"

    assert len(linhas_arquivo1) == len(
        linhas_arquivo2
    ), "Os arquivos têm tamanhos diferentes, podem existir mais diferenças!"

    if not tem_diferenca:
        print(f"\nArquivos{arquivo_base} e{arquivo_atual} são iguais!")

    assert not tem_diferenca, (
        f"\nArquivos com diferenças" f"\n{bytes_diferenca} bytes de diferença"
    )


def comparar_arquivos_excel(
    arquivo_base: str,
    arquivo_atual: str,
    bytes_ignorar: int = 0,
    comparar_headers: bool = True,
) -> None:
    """
    Compara duas planilhas Excel célula a célula, incluindo os cabeçalhos.
    """

    engine_base = "xlrd" if arquivo_base.endswith(".xls") else "openpyxl"
    engine_atual = "xlrd" if arquivo_atual.endswith(".xls") else "openpyxl"

    df_base = pd.read_excel(arquivo_base, engine=engine_base).fillna("")
    df_atual = pd.read_excel(arquivo_atual, engine=engine_atual).fillna("")

    tem_diferenca = False
    bytes_diferenca = 0

    if df_base.shape != df_atual.shape:
        raise AssertionError("As planilhas não têm o mesmo tamanho")

    if comparar_headers:
        headers_base = list(df_base.columns)
        headers_atual = list(df_atual.columns)
        if headers_base != headers_atual:
            print("Diferença nos cabeçalhos:")
            print(f"  Base:{headers_base}")
            print(f"  Atual:{headers_atual}")

    for row_idx in range(df_base.shape[0]):
        for col_idx in range(df_base.shape[1]):

            cell1 = str(df_base.iat[row_idx, col_idx])
            cell2 = str(df_atual.iat[row_idx, col_idx])

            if cell1 != cell2:
                nome_coluna = df_base.columns[col_idx]
                print(
                    f"Diferença na linha{row_idx + 1}, coluna '{nome_coluna}' (índice{col_idx + 1}):"
                )
                print(f"Arquivo Base:{cell1}")
                print(f"Arquivo Atual:{cell2}")

                tem_diferenca = True

    assert not tem_diferenca, "Arquivos Excel possuem diferenças"


def converter_pdf_para_texto(arquivo_pdf: str) -> str:
    """
    Converte um arquivo PDF em texto simples para comparação em testes.
    """

    paginas_texto = []

    try:
        with open(arquivo_pdf, "rb") as f:
            leitor_pdf = PyPDF2.PdfReader(f)

            for pagina in leitor_pdf.pages:
                texto = pagina.extract_text()

                if texto:
                    paginas_texto.append(texto)

    except Exception as e:
        raise RuntimeError(f"Erro ao ler o PDF '{arquivo_pdf}':{e}") from e

    texto_final = "\n".join(paginas_texto)

    texto_final = texto_final.replace("\r", "\n")
    texto_final = re.sub(r"\n+", "\n", texto_final)
    texto_final = re.sub(r"[\t]+", " ", texto_final)
    texto_final = texto_final.strip()

    return texto_final


def converter_e_comparar_pdf(
    arquivo_base: str,
    arquivo_atual: str,
    linhas_ignorar: Optional[list[int]] = None,
    padrao_ignorar: str = "",
    bytes_ignorar: int = 0,
    encoding: str = "utf-8",
) -> None:
    """
    Extrai o texto de PDFs e os compara linha por linha.
    """

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", encoding=encoding, delete=False
    ) as f_atual:
        temp_atual = f_atual.name
        f_atual.write(converter_pdf_para_texto(arquivo_atual))

    temp_base = None

    try:
        if arquivo_base.lower().endswith(".pdf"):
            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".txt", encoding=encoding, delete=False
            ) as f_base:
                temp_base = f_base.name
                f_base.write(converter_pdf_para_texto(arquivo_base))
            base_para_comparar = temp_base
        else:
            base_para_comparar = arquivo_base

        comparar_arquivos(
            base_para_comparar,
            temp_atual,
            linhas_ignorar,
            padrao_ignorar,
            bytes_ignorar,
            encoding=encoding,
        )
    finally:
        os.remove(temp_atual)
        if temp_base and os.path.exists(temp_base):
            os.remove(temp_base)
