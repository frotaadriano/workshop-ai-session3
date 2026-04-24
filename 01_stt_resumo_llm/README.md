# STT + Resumo com LLM

Aplicação demo de workshop para demonstrar, de forma simples e visual, o fluxo:

1. Captura de áudio via microfone no navegador
2. Transcrição com Azure Speech to Text
3. Geração de resumo com Azure OpenAI

---

## Pré-requisitos

- Python 3.9 ou superior
- Uma conta Azure com:
  - Azure Speech Service ativo
  - Azure OpenAI com um deployment de chat configurado

---

## Configuração

1. Copie o arquivo `.env.example` e renomeie para `.env`:
   ```
   copy .env.example .env
   ```

2. Preencha as variáveis no arquivo `.env` com suas credenciais Azure.

---

## Como rodar

```bash
# 1. Criar o ambiente virtual
python -m venv .venv

# 2. Ativar o ambiente virtual (Windows)
.venv\Scripts\activate

# 2.1. Atualizar o pip
python.exe -m pip install --upgrade pip

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Rodar a aplicação
uvicorn app:app --reload
```

Acesse em: [http://localhost:8000](http://localhost:8000)

---

## Fluxo da aplicação

```
Navegador
  └── grava áudio com microfone (MediaRecorder)
  └── envia o arquivo .webm para o backend

Backend (FastAPI)
  └── recebe o áudio
  └── chama Azure Speech to Text (REST API)
  └── obtém a transcrição
  └── chama Azure OpenAI (SDK)
  └── retorna transcrição + resumo

Navegador
  └── exibe transcrição e resumo na tela
```
