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

# Chaveamento HD vs Standard (true = HD, false = Standard)
AZURE_SPEECH_USE_HD=false
AZURE_SPEECH_VOICE_HD=pt-BR-Thalita:DragonHDLatestNeural
AZURE_SPEECH_VOICE_STANDARD=pt-BR-FranciscaNeural
```

### 4. Rode a aplicação na porta 8004

```bash
uvicorn app:app --reload --port 8004
```

Acesse no navegador: [http://localhost:8004](http://localhost:8004)

---

## 🖥️ Como usar a interface

A tela tem **um seletor de voz** que permite experimentar diferentes opções sem reiniciar o servidor:

```
┌──────────────────────────────────────────────────────┐
│  ✏️  Texto de entrada                       [Passo 1] │
│                                                      │
│  Qualidade: [ Standard ] [ HD ✨ ]   Voz: [ ▼ ]      │
│  ┌────────────────────────────────────────────────┐  │
│  │ Cole aqui o texto a ser resumido...            │  │
│  └────────────────────────────────────────────────┘  │
│  [          ▶ Processar          ]                   │
└──────────────────────────────────────────────────────┘
```

### Passo a passo

1. **Escolha a qualidade** clicando em `Standard` ou `HD ✨`
2. **Escolha a voz** no dropdown (a lista muda conforme o tipo selecionado)
3. **Cole ou digite o texto** que você quer resumir
4. Clique em **Processar**

A app vai:
- Gerar o resumo via Azure OpenAI
- Sintetizar o áudio com a voz que você escolheu
- Mostrar texto original, resumo e player de áudio
- Indicar embaixo do player qual voz foi usada (ex: `Tipo: HD | Voz: pt-BR-Thalita:DragonHDLatestNeural`)

### Vozes pt-BR disponíveis na app

| Categoria | Vozes |
|---|---|
| **Standard** | Francisca, Antonio, Brenda, Donato, Elza, Fabio, Giovanna, Humberto, Julio, Leila, Leticia, Manuela, Nicolau, Valerio, Yara |
| **HD** | Thalita HD |

> 💡 Para adicionar mais vozes, edite as listas `VOZES_STANDARD` e `VOZES_HD` no [app.py](app.py).

---

## 🎙️ Tipos de voz no Azure TTS — guia rápido

O Azure Speech oferece **dois tipos principais** de vozes para Text-to-Speech. Esta app suporta ambos via toggle na UI ou pelo `.env` (`AZURE_SPEECH_USE_HD`).

### 1. Voz **Standard (Neural)**

- Exemplos: `pt-BR-FranciscaNeural`, `pt-BR-AntonioNeural`, `pt-BR-BrendaNeural`
- Formato do nome: `<idioma>-<voz>Neural`
- ✅ Mais **rápida** (latência ~500ms)
- ✅ Mais **barata** por caractere
- ✅ Disponível em **dezenas de regiões** Azure
- ✅ Suporta **SSML completo** (prosódia, pausa, ênfase, estilos)
- ✅ **Mais de 500 vozes** em centenas de idiomas
- 🎯 **Ideal para:** demos, produção em larga escala, apps que precisam de baixa latência

### 2. Voz **HD (Dragon HD)**

- Exemplos: `pt-BR-Thalita:DragonHDLatestNeural`, `en-US-Ava:DragonHDLatestNeural`
- Formato do nome: `<idioma>-<voz>:DragonHDLatestNeural` (com **dois pontos `:`**)
- ✨ Som **muito mais natural e humano** (treinado com mais dados)
- ✨ **Detecta emoção** automaticamente do texto
- ✨ Suporta **parâmetros avançados** (`temperature`, `top_p`, etc.)
- ⚠️ Só ~30 personas (ex: Thalita em pt-BR)
- ⚠️ Disponível em **menos regiões** (ex: `swedencentral`, `eastus2`, `westus3`)
- ⚠️ Suporta **subset reduzido de SSML** (sem `<prosody>`, `<emphasis>` etc.)
- ⚠️ Mais **cara** e ligeiramente mais lenta
- 🎯 **Ideal para:** narração premium, audiobooks, customer service, apps com foco em qualidade

### Comparação rápida

| | Standard (Neural) | HD (Dragon HD) |
|---|---|---|
| **Qualidade** | Boa, robótica em alguns trechos | Excelente, quase humana |
| **Latência** | ~500ms | ~300ms (mas +tempo de modelo) |
| **Custo** | $ | $$$ |
| **Vozes pt-BR** | ~15 vozes | 1 voz (Thalita) |
| **SSML** | Completo | Subset |
| **Regiões** | Quase todas | Algumas (ex: swedencentral) |

### Padrão inicial via `.env`

A UI tem prioridade, mas você pode definir o padrão inicial pelo `.env`:

```env
AZURE_SPEECH_USE_HD=false                                       # padrão Standard
AZURE_SPEECH_VOICE_HD=pt-BR-Thalita:DragonHDLatestNeural        # voz HD padrão
AZURE_SPEECH_VOICE_STANDARD=pt-BR-FranciscaNeural               # voz Standard padrão
```

Ao processar, o terminal mostra qual voz foi de fato usada:

```
[TTS] Tipo: Standard (Neural) | Voz: pt-BR-FranciscaNeural | Região: swedencentral
```

### ⚠️ Atenção ao formato do nome

O nome técnico no SSML/REST API segue o padrão oficial Microsoft `<voicename>:<basemodel>:<version>` — **não** é o rótulo exibido no Speech Playground:

| Rótulo no Playground | Nome técnico (SSML) |
|---|---|
| Francisca Neural | `pt-BR-FranciscaNeural` |
| Thalita Dragon HD Latest | `pt-BR-Thalita:DragonHDLatestNeural` |

📚 Documentação oficial: [HD voices Azure Speech](https://learn.microsoft.com/azure/ai-services/speech-service/high-definition-voices)

---

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
