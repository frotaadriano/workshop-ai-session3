# Document Intelligence + Extração Estruturada

Demo didática de leitura e extração de documentos usando **Azure Document Intelligence** + **FastAPI**.

Criada para workshop interno de introdução à IA.

---

## O que a app faz

1. Usuário faz upload de um documento (PDF ou imagem)
2. O backend envia o documento para o Azure Document Intelligence
3. O serviço extrai o texto contido no documento
4. A app exibe o texto extraído e um resumo estruturado na tela

---

## Pré-requisitos

- Python 3.10 ou superior
- Conta no Azure com o serviço **Document Intelligence** criado
- Endpoint e chave de API do serviço

---

## Configuração

1. Copie o arquivo de exemplo de variáveis de ambiente:

```bash
cp .env.example .env
```

2. Preencha o `.env` com suas credenciais do Azure:

```
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://seu-recurso.cognitiveservices.azure.com/
AZURE_DOCUMENT_INTELLIGENCE_KEY=sua-chave-aqui
```

---

## Como rodar

```bash
# 1. Criar ambiente virtual
python -m venv venv
C:\Users\adriano.frota.silva\AppData\Local\Programs\Python\Python310\python.exe -m venv venv

# 2. Ativar o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 2.1. Atualizar o pip
python.exe -m pip install --upgrade pip


# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar a aplicação
uvicorn app:app --reload
```

A app estará disponível em: http://localhost:8000

---

## Estrutura do projeto

```
02_document_intelligence_extracao/
├── app.py                   # Backend FastAPI
├── requirements.txt         # Dependências Python
├── .env.example             # Exemplo de variáveis de ambiente
├── .env                     # Suas credenciais (não versionar!)
├── README.md                # Este arquivo
├── changelog.md             # Histórico de alterações
├── copilot-instructions.md  # Regras do projeto para o Copilot
└── templates/
    └── index.html           # Interface do usuário
```
