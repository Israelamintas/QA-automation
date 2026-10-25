@echo off
title Suite de Testes Pytest - SAP Workflow Automation
color 0B

echo ========================================================
echo  Executando Testes Automatizados (Pytest + SQL Check)
echo ========================================================
echo.

set SCRIPT_DIR=%~dp0
set PROJECT_ROOT=%SCRIPT_DIR%..\..
set REPORT_FILE=%SCRIPT_DIR%..\reports\report.html
set VENV_PYTHON=%SCRIPT_DIR%..\..\.venv_novo\Scripts\python.exe

if not exist "%VENV_PYTHON%" (
    echo [ERRO] Ambiente virtual (.venv_novo) nao encontrado em:
    echo %VENV_PYTHON%
    pause
    exit /b 1
)

cd /d "%PROJECT_ROOT%"

echo Executando testes automatizados com geracao de relatorio HTML...
echo.

"%VENV_PYTHON%" -m pytest Project_Api_Sql_Sap/tests/ -v --html="%REPORT_FILE%" --self-contained-html

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================================
    echo  [SUCESSO] Todos os testes passaram com exito!
    echo ========================================================
) else (
    echo.
    echo ========================================================
    echo  [AVISO/FALHA] Verifique se o servidor esta iniciado (run_server.bat).
    echo ========================================================
)

echo Abrindo relatorio de testes no navegador...
start "" "%REPORT_FILE%"

echo.
pause

