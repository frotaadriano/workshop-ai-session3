# Changelog — AI Search + Mini RAG

## [2.0.0] — 2026-04-28

### Alterado
- `templates/index.html`: reescrita completa da interface com Tailwind CSS CDN + Material Symbols Outlined
  - Header fixo com logo "RAG Insight", nav decorativa e ícones de ação
  - Hero centralizado: título "Exploração Cognitiva", campo de busca com ícone lupa e botão "Consultar →" embutido
  - Step Indicator animado com 5 passos (Pergunta → AI Search → Contexto → LLM → Resposta Final) que acendem em sequência via JS puro
  - Grid 2 colunas: card de trechos (esq.) + card de resposta final (dir.)
  - Badge de score de relevância por trecho (ex: "Score: 0.94")
  - Border-left colorida por posição do trecho (laranja / roxo / cinza)
  - Botão "Copiar" (navigator.clipboard) e botão "Nova Consulta" no card de resposta
  - Banner hero inferior com gradiente roxo→laranja
  - Footer com logo e links decorativos
  - Empty state: grid de resultados oculto até a primeira consulta
- `app.py`: adicionado campo `score` no dicionário de cada trecho em `buscar_trechos_relevantes()`, lendo `@search.score` da resposta do Azure AI Search

### Motivo
Redesign visual para workshop: experiência mais próxima de um produto real, step indicator animado para didática ao vivo, score de relevância visível por trecho.

---

## [1.2.0] — 2026-04-28

### Adicionado
- `templates/index.html` com interface HTML completa:
  - cabeçalho com título e descrição
  - fluxo visual simplificado (5 passos em badges)
  - campo de pergunta com envio por Enter
  - botão "Buscar e Responder" com estado desabilitado durante processamento
  - indicador de status (carregando, sucesso, erro)
  - card para pergunta enviada
  - card para trechos recuperados (Azure AI Search), com título e conteúdo de cada trecho
  - card para resposta final (Azure OpenAI)
  - nota explicativa sobre o fluxo RAG
  - layout limpo com CSS mínimo

### Motivo
Implementação da interface visual para demo do workshop.

---

## [1.1.0] — 2026-04-28

### Adicionado
- `app.py` com o backend FastAPI completo:
  - função `buscar_trechos_relevantes()` — consulta ao Azure AI Search via REST
  - função `montar_prompt_com_contexto()` — monta o prompt com instrução + contexto + pergunta
  - função `gerar_resposta_final()` — chama o Azure OpenAI e retorna a resposta
  - rota `GET /` — exibe a interface HTML
  - rota `POST /perguntar` — orquestra o fluxo RAG completo
  - tratamento de erro para falhas no AI Search e erros gerais
  - comentários em português ao longo de todo o código

### Motivo
Implementação do backend RAG funcional. Fluxo: pergunta → AI Search → prompt com contexto → OpenAI → resposta.

---

## [1.0.0] — 2026-04-28

### Adicionado
- Estrutura inicial do projeto (scaffolding)
- `copilot-instructions.md` com regras permanentes do projeto
- `requirements.txt` com dependências mínimas: fastapi, uvicorn, python-dotenv, requests, openai, jinja2, python-multipart
- `.env.example` com todas as variáveis de ambiente necessárias, incluindo campos configuráveis do índice
- `README.md` com instruções de execução, estrutura do projeto e observações sobre o índice
- `changelog.md` com histórico de alterações (este arquivo)

### Motivo
Criação da espinha dorsal do projeto para o workshop de introdução à IA.
