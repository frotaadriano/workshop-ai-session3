# workshop-ai-session3

Repositório com demos simples e didáticas para uma sessão prática de introdução à IA, usando **Python**, **FastAPI**, **Azure AI Services** e **Azure OpenAI**.

A proposta deste material é mostrar, de forma visual e fácil de entender, como diferentes serviços de IA podem ser combinados em miniaplicações com poucas etapas, foco educacional e código legível.

## Objetivo

Este repositório foi organizado para apoiar uma sessão prática de workshop, como continuação de uma introdução anterior baseada em prompts e experimentação em notebook.

Aqui, a ideia é sair do notebook e mostrar pequenos apps que exemplificam fluxos reais com serviços Azure, mantendo:

- simplicidade
- clareza didática
- poucas dependências
- interface leve
- fácil execução local
- versionamento por etapas

## Demos incluídas

### 01 — STT + Resumo com LLM
Aplicação que grava áudio pelo navegador, envia o áudio ao backend, faz **Speech to Text** e depois gera um **resumo com Azure OpenAI**.

Fluxo:
1. usuário grava a fala no navegador
2. o áudio é enviado ao backend
3. o texto é transcrito
4. a transcrição é resumida por um LLM
5. o resultado é exibido na tela

### 02 — Document Intelligence + Extração Estruturada
Aplicação que recebe um documento simples e usa **Azure Document Intelligence** para extrair o conteúdo, exibindo o texto e uma estrutura resumida na interface.

Fluxo:
1. usuário envia um documento
2. o backend processa o arquivo
3. o serviço extrai o conteúdo
4. o app exibe o texto e informações organizadas

### 03 — AI Search + Mini RAG
Aplicação que demonstra uma forma simples de **busca semântica com Azure AI Search** combinada com geração de resposta usando **Azure OpenAI**, em um fluxo didático de mini RAG.

Fluxo:
1. usuário faz uma pergunta
2. a app consulta o índice no Azure AI Search
3. recupera trechos relevantes
4. monta um prompt com contexto
5. gera uma resposta final com o LLM

### 04 — LLM + TTS
Aplicação que recebe um texto, gera um **resumo com Azure OpenAI** e transforma esse resumo em **áudio com Azure Text to Speech**.

Fluxo:
1. usuário digita ou cola um texto
2. o backend gera um resumo com LLM
3. o resumo é enviado ao TTS
4. a interface exibe o resumo e um player de áudio

## Estrutura do repositório

```text
workshop-ai-session3/
├── 01_stt_resumo_llm/
├── 02_document_intelligence_extracao/
├── 03_ai_search_mini_rag/
├── 04_llm_tts/
├── .gitignore
└── README.md