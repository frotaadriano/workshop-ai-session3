# Copilot Instructions — Document Intelligence Demo
# Projeto: 02_document_intelligence_extracao
# Versão: 1.0 — 2026-04-24

## Contexto do Projeto

Este projeto é uma demo didática criada para um workshop interno de introdução à IA.
O objetivo é demonstrar, de forma simples e visual, como o Azure Document Intelligence
extrai texto de documentos. O público é iniciante em Python e IA.

---

## Regras Permanentes — SIGA SEMPRE

### Simplicidade
- Mantenha o código SEMPRE simples e fácil de entender.
- Prefira clareza em vez de sofisticação.
- Evite abstrações desnecessárias.
- Escreva funções pequenas com responsabilidade única.
- Use nomes de variáveis descritivos em português ou inglês claro.

### Stack obrigatória
- Python + FastAPI + HTML simples
- Azure Document Intelligence (modelo `prebuilt-read`)
- `requests` para chamadas HTTP
- `python-dotenv` para variáveis de ambiente
- Templates Jinja2 apenas se necessário

### Proibido neste projeto
- React, Vue, Angular
- LangChain, LangGraph, Semantic Kernel, LlamaIndex
- Docker, banco de dados, autenticação
- Arquitetura em camadas desnecessária
- Classes complexas
- Excesso de arquivos

### Código
- Comente o código em português.
- Trate erros com mensagens claras para o usuário.
- Sempre revise imports e dependências antes de finalizar.
- Garanta que a aplicação rode com `uvicorn app:app --reload`.
- Sempre valide que o `.env.example` está atualizado com as variáveis usadas.

### Interface
- HTML simples, sem frameworks CSS pesados.
- Layout limpo: título, descrição, upload, botão, áreas de resultado.
- Nenhum JavaScript complexo.

---

## Changelog — REGRA OBRIGATÓRIA

**NENHUMA TAREFA é considerada concluída sem atualizar o `changelog.md`.**

Ao realizar qualquer alteração relevante no projeto:

1. Abra o `changelog.md`.
2. Adicione uma nova entrada com:
   - Marcador da etapa (ex: `[Etapa B]`) e data
   - Resumo do que foi alterado
   - Lista de arquivos criados ou modificados
   - Motivo da alteração
3. Registre qualquer mudança em: interface, backend, dependências, variáveis de ambiente, rotas ou documentação.

Trate o `changelog.md` como artefato obrigatório — não como opcional.

---

## Forma de Trabalho

1. Sempre entenda o que está sendo alterado antes de gerar código.
2. Sempre revise consistência (imports, rotas, variáveis) antes de finalizar.
3. Sempre pense: "um iniciante consegue entender este código?"
4. Após qualquer alteração, proponha também a entrada de changelog correspondente.
5. Documente como rodar a aplicação sempre que houver mudança relevante.
6. Considere que cada etapa pode virar um commit Git separado.

---

## Execução Local

```bash
uvicorn app:app --reload
```

Acesse em: http://localhost:8000
