# # **Integração Contínua**

# ## Objetivo

# Configurar um **pipeline de execução de testes automatizados com Playwright e Python no Jenkins**, utilizando um **job livre** que:

# - Executa testes
# - Gera relatório HTML
# - Salva screenshots e trace no Jenkins

# ---

# ## 1 – Instalação do Jenkins

# ### Passo 1 –Instalar Java

# - **Java 21 ou 24** instalado (`java -version`)

#     https://www.oracle.com/br/java/technologies/downloads/#jdk21-windows


# ---

# ### Passo 2 – Instalar o Jenkins

# **Windows:**

# 1. Baixe o instalador no site oficial:

#     https://www.jenkins.io/download/

# 2. Siga o instalador e inicie o serviço Jenkins.

# ---

# ### Passo 3 – Acessar o Jenkins

# - No navegador:

#     ```
#     http://localhost:8080
#     ```

# - Copie a senha do arquivo indicado no terminal:

#     ```
#     /var/lib/jenkins/secrets/initialAdminPassword
#     ```

# - Instale os **plugins recomendados**.

# ---

# ### Passo 4 – Plugins adicionais

# No menu **Gerenciar Jenkins → Gerenciar Plugins**, instale:

# - **HTML Publisher** (publicar relatórios HTML)

# ---

# ## 2 – Criando o Job

# ### Passo 1 – Novo Job

# 1. **Nova Tarefa** → Digite um nome (ex: `playwright-tests`).
# 2. Tipo: Projeto de software de estilo livre.

# ### Passo 2 – Configurar Job

# 1. Definir um Workspace customizado com o diretorio do nosso projeto
# 2. Em passos de construção adicionar o passo “Executar no comando do Windows”

# ```python
# call venv/Scripts/activate.bat
# pip install -r requirements.txt
# playwright install

# pytest tests/test_adicionar_produtos_ao_carrinho.py
# ```

# ---

# ## 3 – Publicando Relatório e Artefatos no Jenkins

# ### 3.1 Relatório HTML

# 1. No comando do pytest adicione os argumentos:

# ```python
# --html=report.html --self-contained-html
# ```

# 1. Em **Pós-build actions** → **Publish HTML reports**.

# !image.png

# ### Caso o Resultado do HTML fique sem o CSS:

# - Vá em: Jenkins → Manage Jenkins → Script Console
# - Cole e execute:

#     ```groovy
#     System.setProperty("hudson.model.DirectoryBrowserSupport.CSP", "")
#     ```


# ---

# ### 3.2 Arquivos de evidência (video, trace)

# 1. Adicionar a geração do Trace na fixture do conftest.py

# ```python
# @pytest.fixture(scope='session')
# def contexto(browser):
#     if os.path.isfile(STORAGE_FILE):
#         contexto = browser.new_context(
#             base_url='https://automationexercise.com/',
#             record_video_dir='videos',
#             storage_state=STORAGE_FILE
#         )
#     else:
#         contexto = browser.new_context(
#             base_url='https://automationexercise.com/',
#             record_video_dir='videos'
#         )
#     contexto.tracing.start(screenshots=True, snapshots=True, sources=True)
#     yield contexto

#     os.makedirs(os.path.dirname(STORAGE_FILE), exist_ok=True)
#     contexto.tracing.stop(path='trace/trace.zip')
#     if not os.path.isfile(STORAGE_FILE):
#         contexto.storage_state(path=STORAGE_FILE)

#     contexto.close()
# ```

# 1. Em **Pós-build actions**, adicione **Archive the artifacts**.
# 2. Em **Files to archive**, coloque:

#     ```
#     trace/trace.zip, videos/*.webm
#     ```
