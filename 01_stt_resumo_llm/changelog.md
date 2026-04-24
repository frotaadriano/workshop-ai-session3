# Changelog — STT + Resumo com LLM

## [1.3.0] — 2026-04-24

### Corrigido
- Removido HTML antigo duplicado que estava colado após o `</html>` da nova UI, causando renderização incorreta da página

---

## [1.2.0] — 2026-04-24

### Alterado
- Reescrita completa do `templates/index.html` com nova identidade visual inspirada em Avanade (laranja `#FF6B00`, roxo `#6B2D8B`)
- Adicionado indicador de etapas (Step Indicator) com 3 estados visuais: ativo, concluído e pendente
- Adicionado barra de status colorida por contexto (gravando / processando / sucesso / erro)
- Adicionado ícone de microfone com animação de pulse durante gravação
- Adicionado badge exibindo tamanho e formato do áudio gravado
- Cards lado a lado para Transcrição (STT) e Resumo (IA)

### Corrigido
- Corrigida causa raiz do STT retornar vazio: o `MediaRecorder` grava em WebM/Opus, que o Azure STT não suporta de forma garantida
- Adicionada conversão de WebM → WAV PCM 16kHz mono no próprio navegador via `AudioContext` antes do envio
- Backend atualizado para passar o `content-type` correto (`audio/wav`) na chamada ao Azure STT
- Adicionada verificação do campo `RecognitionStatus` na resposta do Azure STT
- Adicionada validação de tamanho mínimo do áudio no backend (< 1 KB = erro claro)

---

## [1.1.0] — 2026-04-24

### Corrigido
- Erro 500 na rota `GET /`: `TemplateResponse` do Starlette ≥ 0.36 mudou de assinatura
  - **Antes (quebrado):** `templates.TemplateResponse("index.html", {"request": request})`
  - **Depois (correto):** `templates.TemplateResponse(request, "index.html")`

---

## [1.0.0] — 2026-04-24

### Adicionado
- Estrutura inicial do projeto
- `app.py` com FastAPI, rota GET `/` e rota POST `/processar`
- Integração com Azure Speech to Text via API REST
- Integração com Azure OpenAI via SDK oficial
- `templates/index.html` com interface simples e gravação de áudio via MediaRecorder
- `requirements.txt` com dependências mínimas
- `.env.example` com variáveis de ambiente necessárias
- `copilot-instructions.md` com regras do projeto
- `README.md` com instruções de execução
