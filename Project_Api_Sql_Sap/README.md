# 📦 Enterprise Purchase Order & Stock Management System
> **Portfólio de Engenharia de Qualidade (QA Automation & Backend)**  
> Inspirado em processos reais de compras, pagamentos e estoques do **SAP (Módulos MM/FI)**.

---

## 🎯 Visão Geral do Projeto

Este projeto demonstra um ciclo de engenharia completo:
1. **Backend Próprio (API REST)** construído com **FastAPI + Uvicorn + SQLite**.
2. **Framework de Testes Automatizados** construído com **Pytest + Requests**.
3. **Validação de Banco de Dados de Caixa-Branca** (*Database Assertions*) com queries SQL diretas.
4. **Visão Futura**: Testes E2E/UI com **Playwright** e **Selenium WebDriver** cobrindo o Swagger e fluxos web, com automação contínua via **GitHub Actions (CI/CD)** e atalhos de execução rápida para Windows (`.bat`).

---

## 🏗️ Arquitetura e Estrutura de Pastas

```text
Project_Api_Sql_Sap/
├── backend/                             # 🚀 Servidor de Aplicação (API REST)
│   ├── db.py                            # Inicialização e conexões com SQLite (purchase_orders.db)
│   ├── models.py                        # Contratos e validações com Pydantic (Field, tipos e regras)
│   ├── main.py                          # Ponto de entrada FastAPI + Uvicorn
│   └── routers/                         # Endpoints modulares de negócio
│       ├── suppliers.py                 # Gestão de Fornecedores (CRUD)
│       ├── products.py                  # Gestão de Produtos e consulta de estoque
│       └── purchase_orders.py           # Ciclo de vida e Workflow de Ordens de Compra
│
├── tests/                               # 🧪 Suite de Testes Automatizados (Pytest)
│   ├── configs.py                       # Configurações de ambiente (BASE_URL e caminho do banco)
│   ├── clients/                         # Clientes reutilizáveis
│   │   ├── api_client.py                # Wrapper HTTP sobre a biblioteca requests
│   │   └── sql_client.py                # Leitor e validador direto do SQLite
│   ├── helpers/                         # Fábricas de payloads e utilitários de teste
│   │   └── po_helper.py                 # Gerador de dados dinâmicos com UUID (evita 409 UNIQUE)
│   ├── conftest.py                      # Fixtures do Pytest (api_client e sql_client)
│   ├── test_suppliers.py                # ✅ Testes de fornecedores (CRUD + SQL check) [4/4 PASSING]
│   ├── test_products.py                 # ✅ Testes de produtos e regras de estoque [5/5 PASSING]
│   └── test_po_workflow.py              # ✅ Testes da máquina de estados SAP e auditoria [4/4 PASSING]
│
├── reports/                             # 📊 Relatórios HTML de execução de testes
│   └── report.html                      # Relatório visual gerado pelo pytest-html (13 testes verdes)
│
├── scripts/                             # ⚡ Scripts de automação local para Windows (.bat)
│   ├── run_server.bat                   # Inicia o servidor local com 2 cliques
│   └── run_tests.bat                    # Roda os 13 testes e abre relatório HTML com 2 cliques
│
├── requirements.txt                     # 📦 Dependências do projeto (FastAPI, Pytest, etc.)
│
└── .github/workflows/sap-api-tests.yml  # 🚀 Pipeline de CI/CD automática (GitHub Actions)
```

---

## 🧭 Mapa de Progresso do Projeto

| Fase | Descrição | Status | Detalhes |
| :--- | :--- | :---: | :--- |
| **Fase 1** | **Backend Mínimo & Banco de Dados** | ✅ Concluído | SQLite estruturado, Pydantic com `Field`, Swagger ativo em `http://127.0.0.1:8000/docs`. |
| **Fase 2** | **Workflow de Compras (Máquina de Estados)** | ✅ Concluído | Fluxo `draft` ➔ `pending_approval` ➔ `approved` ➔ `received` (atualiza estoque e gera auditoria `stock_movements`). |
| **Fase 3** | **Framework de Automação de Testes (Pytest)** | ✅ **CONCLUÍDO** | `test_suppliers.py`, `test_products.py` e `test_po_workflow.py` (Total de 13 testes cobrindo todo o ciclo SAP). |
| **Fase 4** | **Testes E2E (Playwright & Selenium)** | 🟡 **PRÓXIMO PASSO** | Automação no Swagger UI (`/docs`) e validações de tela com navegadores reais. |
| **Fase 5** | **Entrega: Tags Git, PR, `.bat` e CI/CD** | 🟡 **EM ANDAMENTO** | Scripts `.bat` prontos, CI/CD GitHub Actions configurada. Pronto para Tag `v1.0.0` e Pull Request! |

> **📍 Onde estamos exatamente agora:**  
> A suíte completa de **13 testes do Pytest com validação no SQLite** está finalizada e funcional.  
> Criamos os scripts de 2 cliques para Windows (`run_server.bat` e `run_tests.bat`) e a esteira de CI/CD do GitHub Actions!  
> **Próximo passo imediato:** Fase 4 — Testes E2E com **Playwright** interagindo com a interface gráfica do Swagger UI!

---

## 🚀 Como Executar os Testes e Gerar Relatórios

Para rodar os testes a qualquer momento a partir da raiz do projeto (`QA-automation`), use o terminal PowerShell:

```powershell
# 1. Executar todos os testes no terminal com detalhes (-v)
.\.venv_novo\Scripts\python.exe -m pytest Project_Api_Sql_Sap/tests/ -v

# 2. Executar apenas os testes de fornecedores
.\.venv_novo\Scripts\python.exe -m pytest Project_Api_Sql_Sap/tests/test_suppliers.py -v

# 3. Executar e gerar um Relatório Visual HTML completo
.\.venv_novo\Scripts\python.exe -m pytest Project_Api_Sql_Sap/tests/ --html=Project_Api_Sql_Sap/reports/report.html --self-contained-html
```
*(Nota: Esse comando para gerar relatório também será empacotado no script `run_tests.bat` para execução com 2 cliques).*

---

## 💡 Ideias & Decisões Registadas Durante o Projeto

1. **Domínio de Negócio Real (SAP MM/FI)**: Em vez de projetos genéricos de curso (*Petstore*, *Job Tracker*), o tema foca em **Compras e Gestão de Estoque**, alinhando-se aos 3 anos de experiência do autor.
2. **Máquina de Estados Estrita**:
   - Uma ordem só pode ser recebida se estiver `approved`.
   - Ao receber (`/receive`), o estoque é incrementado e uma movimentação `INBOUND` é gerada com segurança transacional (`commit`/`rollback`).
3. **Testes em Dupla Camada (API + SQL)**:
   - O `api_client.py` valida o retorno HTTP e o JSON.
   - O `sql_client.py` consulta diretamente o SQLite para garantir que o dado foi persistido no disco.
4. **Facilidade no Windows**:
   - Criação de scripts `.bat` para inicialização imediata sem comandos manuais no terminal.
5. **Expansão para Testes de UI**:
   - Uso de **Playwright** e **Selenium** sobre a interface do Swagger UI (`/docs`) e validações de tela.
6. **Isolamento de Dados em Testes com UUID**:
   - Para respeitar as restrições `UNIQUE` do banco de dados sem precisar apagar a base a cada teste, usamos geradores com sufixos dinâmicos (`uuid.uuid4().hex[:6]`). Isso garante idempotência e impede erros 409 (*Conflict*) em execuções repetidas.
7. **Autenticação, Criptografia e Perfis (Ideia Futura - Segurança & Segregação de Funções)**:
   - Implementação de tabela de usuários com senhas criptografadas (hashing via `bcrypt` / `passlib`).
   - Autenticação via JWT Tokens (`Bearer Token`).
   - Segregação de Funções (SoD do SAP): perfis distintos de acesso (`buyer` cria a ordem, `approver/manager` aprova, `warehouse` realiza o recebimento físico no estoque).
8. **Relatórios Visuais de Execução de Testes**:
   - Integração do plugin `pytest-html` para geração de relatórios ricos (`reports/report.html`) executáveis com comando único ou via script `.bat`.
