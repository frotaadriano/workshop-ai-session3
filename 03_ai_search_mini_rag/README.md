# AI Search + Mini RAG

Demonstração didática de um fluxo RAG (Retrieval-Augmented Generation) usando:
- **Azure AI Search** — para buscar trechos relevantes em uma base de conhecimento
- **Azure OpenAI** — para gerar a resposta final com base no contexto recuperado

> **Este projeto é uma demo para workshop.** O foco é clareza e didática, não produção.

---

## O que esta aplicação faz?

1. Você digita uma pergunta na interface
2. O backend busca os trechos mais relevantes no **Azure AI Search**
3. Os trechos são usados para montar um prompt com contexto
4. O prompt é enviado ao **Azure OpenAI**
5. A resposta final é exibida junto com os trechos que a sustentaram

---

## Estrutura do projeto

```
03_ai_search_mini_rag/
├── app.py                  # Backend FastAPI com o fluxo RAG
├── requirements.txt        # Dependências Python
├── .env.example            # Variáveis de ambiente necessárias
├── README.md               # Este arquivo
├── changelog.md            # Histórico de alterações
├── copilot-instructions.md # Regras permanentes do projeto
└── templates/
    └── index.html          # Interface HTML simples
```

---

## Pré-requisitos

- Python 3.10 ou superior
- Um índice criado no **Azure AI Search** com campos `title` e `content`
- Um deployment de modelo de chat no **Azure OpenAI** (ex: `gpt-4o`, `gpt-35-turbo`)

---

## Como rodar localmente

### 1. Criar e ativar o ambiente virtual

```bash
# Criar o venv
python -m venv venv

# Ativar no Windows
venv\Scripts\activate

# Atualizar o pip
python.exe -m pip install --upgrade pip

# Ativar no Linux/Mac
source venv/bin/activate
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar as variáveis de ambiente

Copie o arquivo `.env.example` para `.env` e preencha com seus dados:

```bash
cp .env.example .env
```

Edite o arquivo `.env` com suas credenciais do Azure.

### 4. Rodar a aplicação porta 8003

```bash
uvicorn app:app --reload --port 8003 
```

Acesse no navegador: [http://localhost:8000](http://localhost:8000)

---

## Observação sobre os campos do índice

Por padrão, a aplicação espera que seu índice no Azure AI Search tenha os campos:
- `content` — o texto do documento
- `title` — o título ou identificador do documento

Se os seus campos tiverem nomes diferentes, ajuste as variáveis no arquivo `.env`:

```
AZURE_SEARCH_CONTENT_FIELD=meu_campo_de_conteudo
AZURE_SEARCH_TITLE_FIELD=meu_campo_de_titulo
```

---

## Sugestões de commits Git por etapa

```bash
git add .
git commit -m "etapa 1: scaffolding inicial do projeto"

# após implementar o backend
git commit -m "etapa 2: implementação do backend RAG"

# após implementar a interface
git commit -m "etapa 3: interface final e integração completa"
```
