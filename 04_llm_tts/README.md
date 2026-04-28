# LLM + TTS — Demo Workshop IA

Demonstração simples e didática que combina **Azure OpenAI** (geração de resumo) com **Azure Speech TTS** (síntese de voz).

## O que essa app faz

1. Você cola um texto (e-mail, comunicado, notícia etc.)
2. O **Azure OpenAI** gera um resumo curto e objetivo
3. O **Azure Speech TTS** converte o resumo em áudio
4. A tela exibe o texto original, o resumo e um player para ouvir o áudio

## Pré-requisitos

- Python 3.10 ou superior
- Conta Azure com:
  - Azure OpenAI (com um deployment de chat, ex: `gpt-4o`)
  - Azure Speech Service (para TTS)

## Instalação e execução

### 1. Crie e ative o ambiente virtual

```bash
# Ativar no Windows
venv\Scripts\activate

# Atualizar o pip
python.exe -m pip install --upgrade pip
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

```bash
# Copie o arquivo de exemplo
copy .env.example .env      # Windows
cp .env.example .env        # Linux/macOS
```

Edite o `.env` com suas chaves reais:

```env
AZURE_OPENAI_API_KEY=...
AZURE_OPENAI_ENDPOINT=https://seu-recurso.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_CHAT_DEPLOYMENT=gpt-4o

AZURE_SPEECH_KEY=...
AZURE_SPEECH_REGION=eastus
AZURE_SPEECH_VOICE_NAME=pt-BR-FranciscaNeural
```

### 4. Rode a aplicação na porta 8004

```bash
uvicorn app:app --reload --port 8004
```

Acesse no navegador: [http://localhost:8000](http://localhost:8000)

## Estrutura do projeto

```
04_llm_tts/
├── app.py                  # Backend FastAPI (LLM + TTS)
├── requirements.txt        # Dependências Python
├── .env.example            # Modelo de variáveis de ambiente
├── README.md               # Este arquivo
├── changelog.md            # Histórico de alterações
├── copilot-instructions.md # Regras permanentes do projeto
└── templates/
    └── index.html          # Interface HTML com player de áudio
```

## Fluxo técnico resumido

```
[Usuário digita texto]
        ↓
  POST /processar
        ↓
  gerar_resumo()   → Azure OpenAI (chat completion)
        ↓
  gerar_audio()    → Azure Speech TTS (síntese de voz)
        ↓
  Retorna JSON { resumo, audio_base64 }
        ↓
  Frontend exibe resumo + player HTML5
```

## Sugestões de commits Git

```bash
git add .
git commit -m "feat: estrutura inicial do projeto LLM + TTS"

# após a integração LLM
git commit -m "feat: integração com Azure OpenAI para geração de resumo"

# após a integração TTS
git commit -m "feat: integração com Azure Speech TTS e player de áudio"
```
