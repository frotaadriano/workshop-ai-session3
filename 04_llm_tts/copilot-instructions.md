# copilot-instructions.md — Regras permanentes do projeto

## Contexto do projeto
Este é um projeto demo para workshop de introdução à IA.
O objetivo é demonstrar um fluxo simples de LLM + TTS de forma didática:
1. Usuário digita um texto
2. Azure OpenAI gera um resumo curto
3. Azure Speech TTS converte o resumo em áudio
4. A interface exibe o texto original, o resumo e um player de áudio

## Regras obrigatórias

### Simplicidade acima de tudo
- Manter o app simples e didático — é para workshop, não para produção
- Evitar arquitetura em camadas, classes complexas ou abstrações desnecessárias
- Não adicionar features que não foram pedidas explicitamente

### Stack obrigatória
- Python + FastAPI para o backend
- HTML simples + JavaScript nativo no frontend
- Azure OpenAI (via SDK oficial `openai`)
- Azure Speech Text to Speech (via SDK `azure-cognitiveservices-speech`)
- `python-dotenv` para variáveis de ambiente
- `Jinja2` para templates HTML

### Stack proibida
- Não usar: React, Vue, Angular, LangChain, LangGraph, Semantic Kernel, LlamaIndex
- Não usar: Docker, banco de dados, autenticação, WebSocket
- Não usar: frameworks de frontend pesados
- Não usar: streaming de áudio em tempo real ou WebRTC

### Código
- Comentários sempre em português
- Funções pequenas, com responsabilidade única
- Nomes de variáveis descritivos e claros
- Legibilidade acima de performance

### Processo
- Sempre revisar consistência (imports, dependências, rotas) antes de finalizar
- **SEMPRE atualizar o `changelog.md` após cada mudança significativa**
- **NUNCA considerar uma tarefa concluída sem atualizar o `changelog.md`**
- Sempre documentar como rodar no `README.md`
- Sempre considerar execução local (sem Docker, sem cloud deploy)
- Sempre testar/buildar após mudanças, quando aplicável
- Ao final de cada etapa, revisar se o changelog foi atualizado

### Changelog (artefato obrigatório)
- Toda alteração relevante (interface, backend, dependências, variáveis, rotas, docs) DEVE entrar no `changelog.md`
- Registrar: data/etapa, resumo do que foi alterado, arquivos criados ou modificados, motivo
- O changelog é parte obrigatória da implementação, não opcional
- Se o changelog não for atualizado, a tarefa está incompleta

### Git
- Versionar cada etapa do workshop com commits separados
- Mensagens de commit claras e em português
