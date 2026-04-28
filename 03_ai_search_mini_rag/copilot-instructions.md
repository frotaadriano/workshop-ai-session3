# copilot-instructions.md — Regras permanentes do projeto

## Contexto do projeto
Este é um projeto demo para workshop de introdução à IA.
O objetivo é demonstrar um fluxo simples de busca semântica com RAG (Retrieval-Augmented Generation)
usando Azure AI Search + Azure OpenAI, de forma visual e didática.

## Regras obrigatórias

### Simplicidade acima de tudo
- Manter o app simples e didático — é para workshop, não para produção
- Evitar arquitetura em camadas, classes complexas ou abstrações desnecessárias
- Não adicionar features que não foram pedidas explicitamente
- Comentários sempre em português — o código deve ser legível para iniciantes

### Stack obrigatória
- Python + FastAPI para o backend
- HTML simples + JavaScript nativo no frontend (sem frameworks)
- Azure AI Search (via REST com `requests`)
- Azure OpenAI (via SDK oficial `openai`)
- `python-dotenv` para variáveis de ambiente
- Jinja2 para templates HTML (já incluído no FastAPI)

### Stack proibida
- NÃO usar: React, Vue, Angular
- NÃO usar: LangChain, LangGraph, Semantic Kernel, LlamaIndex
- NÃO usar: Docker, banco de dados, autenticação, classes complexas
- NÃO usar: frameworks de frontend pesados ou bundlers (webpack, vite, etc.)

### Código
- Funções pequenas, com responsabilidade única
- Nomes de variáveis descritivos e em português sempre que possível
- Legibilidade acima de performance
- Sem over-engineering: se algo pode ser feito em 10 linhas, use 10 linhas

### Processo de desenvolvimento
- Sempre revisar consistência (imports, dependências, rotas) antes de finalizar
- Sempre considerar execução local (sem Docker, sem cloud deploy)
- Sempre testar/buildar após mudanças, quando aplicável
- Pensar sempre: "um iniciante consegue ler e entender isso?"

---

## CHANGELOG — REGRA CRÍTICA

**NENHUMA TAREFA É CONSIDERADA CONCLUÍDA SEM ATUALIZAR O `changelog.md`.**

- Toda alteração relevante DEVE gerar uma entrada no `changelog.md`
- Se você alterar: interface, backend, dependências, variáveis de ambiente, rotas ou documentação → deve entrar no changelog
- O formato deve ser simples: versão/etapa, data, o que foi feito, arquivos afetados, motivo
- Trate o changelog como artefato obrigatório do projeto, não como opcional
- Ao finalizar qualquer tarefa, revisar: "o changelog foi atualizado?"

---

## Git
- Versionar cada etapa do workshop com commits separados
- Mensagens de commit claras e em português
- Sugestão de commits por etapa:
  - `git commit -m "etapa 1: scaffolding inicial do projeto"`
  - `git commit -m "etapa 2: implementação do backend RAG"`
  - `git commit -m "etapa 3: interface final e integração completa"`
