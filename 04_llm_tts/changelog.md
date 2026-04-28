# Changelog — LLM + TTS

## [1.8.1] — 2026-04-28

### Documentação
- Adicionada seção **"Como usar a interface"** no `README.md` com:
  - Diagrama ASCII da nova UI com seletor de voz
  - Passo a passo de uso (escolher qualidade → escolher voz → digitar texto → processar)
  - Tabela com as 16 vozes pt-BR disponíveis na app
  - Dica para adicionar novas vozes editando o `app.py`
- Reorganizada a seção de tipos de voz: agora explica que o **toggle da UI tem prioridade** e o `.env` apenas define o padrão inicial

### Arquivos modificados
- `README.md` — nova seção de uso da interface

---

## [1.8.0] — 2026-04-28

### Adicionado
- **Seletor de voz na própria interface** — agora a UI permite escolher dinamicamente:
  - **Toggle HD vs Standard** (botões com estilo "pill")
  - **Dropdown de vozes** que se atualiza automaticamente conforme o tipo selecionado
  - 15 vozes Standard pt-BR (Francisca, Antonio, Brenda, Donato, Elza, Fabio, Giovanna, Humberto, Julio, Leila, Leticia, Manuela, Nicolau, Valerio, Yara)
  - 1 voz HD pt-BR (Thalita Dragon HD)
- Catálogo de vozes definido no `app.py` (`VOZES_STANDARD`, `VOZES_HD`) e injetado no template via Jinja
- Endpoint `/processar` agora aceita `voz` e `usar_hd` no body (com fallback para o `.env`)
- Resposta do `/processar` retorna `voz_usada` e `tipo_voz` para a UI exibir
- Card de áudio mostra qual voz foi usada após a síntese

### Alterado
- `app.py`: função `gerar_audio(texto, voz, usar_hd)` agora recebe parâmetros explícitos
- `templates/index.html`: novo card de seleção de voz acima do textarea, novos estilos CSS para toggle e select

### Arquivos modificados
- `app.py` — catálogo de vozes, novos parâmetros em `gerar_audio`, contexto Jinja
- `templates/index.html` — UI de seleção de voz, novo CSS, JS atualizado

---

## [1.7.0] — 2026-04-28

### Adicionado
- **Chaveamento entre vozes HD e Standard** via flag `AZURE_SPEECH_USE_HD` no `.env`
  - `false` → usa voz Standard (`pt-BR-FranciscaNeural`) — rápida e barata
  - `true`  → usa voz HD (`pt-BR-Thalita:DragonHDLatestNeural`) — premium
- Novas variáveis de ambiente: `AZURE_SPEECH_VOICE_HD` e `AZURE_SPEECH_VOICE_STANDARD`
- Removida variável antiga `AZURE_SPEECH_VOICE_NAME`
- Log no terminal mostra qual tipo de voz está ativo: `[TTS] Tipo: Standard (Neural) | Voz: ...`
- Seção didática completa no `README.md` explicando os dois tipos de TTS, comparação, formato dos nomes e como alternar

### Validado
- Voz Standard `pt-BR-FranciscaNeural` → HTTP 200, áudio gerado com sucesso
- Voz HD `pt-BR-Thalita:DragonHDLatestNeural` → HTTP 200, áudio gerado com sucesso
- Ambos os modos funcionam pela mesma rota `/processar`

### Arquivos modificados
- `app.py` — chaveamento HD/Standard via env var
- `.env` — novas variáveis de configuração
- `.env.example` — atualizado com as novas variáveis
- `README.md` — adicionada seção "Tipos de voz no Azure TTS — guia rápido"

---

## [1.6.0] — 2026-04-28

### Corrigido — CAUSA RAIZ DEFINITIVA
- **Nome da voz Dragon HD estava no formato errado**
  - Errado: `pt-BR-ThalitaDragonHDLatest` (nome amigável do Speech Playground)
  - Correto: `pt-BR-Thalita:DragonHDLatestNeural` (formato oficial `voicename:basemodel:version`)
  - Confirmado pela [documentação oficial Microsoft](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/high-definition-voices)
  - Por isso o Azure retornava 400 com corpo vazio — falhava no parse do nome da voz

### Revertido
- Voltou `X-Microsoft-OutputFormat` para `audio-24khz-96kbitrate-mono-mp3` (24kHz é suportado em HD voices)

### Arquivos modificados
- `.env` — corrigido `AZURE_SPEECH_VOICE_NAME`
- `.env.example` — corrigido `AZURE_SPEECH_VOICE_NAME`
- `app.py` — formato de áudio voltou para 24kHz

---

## [1.5.0] — 2026-04-28

### Corrigido
- Erro HTTP 400 na REST API do Azure TTS com corpo vazio
  - Causa raiz: vozes Dragon HD **não suportam formatos 24kHz** — exigem **48kHz mínimo**
  - Alterado `X-Microsoft-OutputFormat` de `audio-24khz-96kbitrate-mono-mp3` para `audio-48khz-96kbitrate-mono-mp3`

### Arquivos modificados
- `app.py` — formato de saída do áudio atualizado para 48kHz

---

## [1.4.0] — 2026-04-28

### Corrigido
- Erro HTTP 400 na REST API do Azure TTS com dois problemas:
  1. **Namespace faltando**: vozes Dragon HD exigem `xmlns:mstts="http://www.w3.org/2001/mstts"` no SSML
  2. **Caracteres XML inválidos**: o resumo gerado pelo LLM pode conter `&`, `<`, `>` que quebram o XML
  - Adicionado `html.escape()` no texto antes de inserir no SSML

### Arquivos modificados
- `app.py` — SSML atualizado com namespace `mstts` e `html.escape()` no texto

---

## [1.3.0] — 2026-04-28

### Corrigido
- Erro `Unsupported voice pt-BR-ThalitaDragonHDLatest` persistia mesmo com SSML
  - Causa raiz: o SDK Azure Speech usa WebSocket, que **não suporta vozes Dragon HD**
  - Solução: substituída a integração TTS do SDK pelo **REST API do Azure Speech**
  - A REST API suporta todas as vozes, incluindo Dragon HD Latest

### Alterado
- Função `gerar_audio` reescrita para usar `requests.post` à REST API TTS (mais simples e didática)
- Formato de saída do áudio alterado de `.wav` para `.mp3` (`audio-24khz-96kbitrate-mono-mp3`)
- Frontend: corrigido MIME type do player de `audio/wav` para `audio/mpeg`
- `requirements.txt`: removido `azure-cognitiveservices-speech`, adicionado `requests==2.32.3`

### Arquivos modificados
- `app.py` — função `gerar_audio` usa REST API em vez do SDK
- `templates/index.html` — MIME type do player corrigido para `audio/mpeg`
- `requirements.txt` — dependências atualizadas

---

## [1.2.0] — 2026-04-28

### Corrigido
- Erro `Unsupported voice pt-BR-ThalitaDragonHDLatest`: vozes Dragon HD não suportam `speak_text_async`
  - Substituído por `speak_ssml_async` com envelope SSML (`<speak>/<voice>`)
  - A voz é especificada diretamente no SSML, sem usar `speech_synthesis_voice_name`

### Arquivos modificados
- `app.py` — função `gerar_audio` atualizada para usar SSML

---

## [1.1.0] — 2026-04-28

### Corrigido
- Erro `Client.__init__() got an unexpected keyword argument 'proxies'` causado por incompatibilidade entre `openai==1.51.0` e `httpx>=0.28`
  - Adicionado `httpx<0.28.0` ao `requirements.txt` para pinar na versão 0.27.x

### Alterado
- Voz TTS atualizada de `pt-BR-FranciscaNeural` para `pt-BR-ThalitaDragonHDLatest` (voz HD premium)
- Região do Azure Speech atualizada de `eastus` para `swedencentral`

### Arquivos modificados
- `requirements.txt` — adicionado `httpx<0.28.0`
- `.env` — atualizado `AZURE_SPEECH_VOICE_NAME` e `AZURE_SPEECH_REGION`
- `.env.example` — atualizado `AZURE_SPEECH_VOICE_NAME` e `AZURE_SPEECH_REGION`

---

## [1.0.0] — 2026-04-28

### Adicionado
- `app.py` — backend FastAPI com:
  - Rota `GET /` servindo a interface HTML via Jinja2
  - Rota `POST /processar` recebendo o texto, gerando resumo e áudio
  - Função `gerar_resumo(texto)` integrando Azure OpenAI (chat completion)
  - Função `gerar_audio(texto)` integrando Azure Speech TTS (síntese de voz em `.wav`)
  - Retorno JSON com `resumo` e `audio_base64` para o frontend
  - Tratamento de erros com mensagens legíveis
- `templates/index.html` — interface HTML com:
  - Indicador visual de etapas (Texto → Resumo → Áudio)
  - Textarea para entrada de texto
  - Botão "Processar"
  - Barra de status visual (processando / sucesso / erro)
  - Cards lado a lado para texto original e resumo gerado
  - Player de áudio HTML5 com o resultado do TTS
  - Layout responsivo e identidade visual laranja
- `requirements.txt` — dependências: fastapi, uvicorn, python-dotenv, openai, azure-cognitiveservices-speech, jinja2, python-multipart
- `.env.example` — modelo com todas as variáveis necessárias: Azure OpenAI e Azure Speech
- `README.md` — instruções de instalação, configuração e execução local
- `copilot-instructions.md` — regras permanentes do projeto (simplicidade, didática, changelog obrigatório)
- `changelog.md` — este arquivo

### Motivo
Criação inicial do projeto para demo de workshop interno de IA.
