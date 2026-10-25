@echo off
title Servidor FastAPI - Purchase Order & Stock Management API
color 0A

echo ========================================================
echo  Iniciando Servidor FastAPI (Backend - SAP Workflow)
echo ========================================================
echo.

set SCRIPT_DIR=%~dp0
set BACKEND_DIR=%SCRIPT_DIR%..\backend
set VENV_UVICORN=%SCRIPT_DIR%..\..\.venv_novo\Scripts\uvicorn.exe

if not exist "%VENV_UVICORN%" (
    echo [ERRO] Ambiente virtual (.venv_novo) nao encontrado em:
    echo %VENV_UVICORN%
    pause
    exit /b 1
)

cd /d "%BACKEND_DIR%"
echo Servidor rodando em: http://127.0.0.1:8000
echo Swagger UI interativo: http://127.0.0.1:8000/docs
echo Pressione CTRL+C para encerrar o servidor.
echo.

"%VENV_UVICORN%" main:app --reload --port 8000
pause

