# Changelog — STT + Resumo com LLM

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
