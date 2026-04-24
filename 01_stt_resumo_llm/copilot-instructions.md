# copilot-instructions.md — Regras permanentes do projeto

## Contexto do projeto
Este é um projeto demo para workshop de introdução à IA.
O objetivo é demonstrar um fluxo simples de STT + LLM de forma didática.

## Regras obrigatórias

### Simplicidade acima de tudo
- Manter o app simples e didático — é para workshop, não para produção
- Evitar arquitetura em camadas, classes complexas ou abstrações desnecessárias
- Não adicionar features que não foram pedidas explicitamente

### Stack obrigatória
- Python + FastAPI para o backend
- HTML simples + JavaScript nativo no frontend
- Azure Speech to Text (via REST)
- Azure OpenAI (via SDK oficial `openai`)
- `python-dotenv` para variáveis de ambiente

### Stack proibida
- Não usar: React, Vue, Angular, LangChain, LangGraph, Semantic Kernel, LlamaIndex
- Não usar: Docker, banco de dados, autenticação, WebSocket
- Não usar: frameworks de frontend pesados

### Código
- Comentários sempre em português
- Funções pequenas, com responsabilidade única
- Nomes de variáveis descritivos e em português
- Legibilidade acima de performance

### Processo
- Sempre revisar consistência (imports, dependências, rotas) antes de finalizar
- Sempre atualizar o `changelog.md` após cada mudança significativa
- Sempre documentar como rodar no `README.md`
- Sempre considerar execução local (sem Docker, sem cloud deploy)
- Sempre testar/buildar após mudanças, quando aplicável

### Git
- Versionar cada etapa do workshop com commits separados
- Mensagens de commit claras e em português
