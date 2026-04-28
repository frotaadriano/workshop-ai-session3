# Changelog

Histórico de alterações do projeto "Document Intelligence + Extração Estruturada".

---

## [Etapa A] — 2026-04-24 — Estrutura inicial do projeto

### Arquivos criados
- `app.py` — esqueleto inicial com FastAPI e rota GET `/`
- `requirements.txt` — dependências do projeto
- `README.md` — instruções de execução e visão geral do projeto
- `changelog.md` — este arquivo
- `.env.example` — exemplo de variáveis de ambiente necessárias
- `copilot-instructions.md` — regras permanentes do projeto para o Copilot
- `templates/index.html` — estrutura HTML inicial da interface

### Motivo
Scaffolding inicial do projeto para o workshop. Base pronta para versionamento e para as próximas etapas de implementação.

---

## [Etapa B+C] — 2026-04-24 — Rota de upload e integração com Azure Document Intelligence

### Arquivos modificados
- `app.py` — adicionada rota `POST /processar`, funções `chamar_document_intelligence`, `extrair_texto_do_resultado` e `montar_informacoes_estruturadas`

### O que mudou
- Rota `POST /processar` recebe o arquivo via upload e dispara o processamento
- Integração com o endpoint `prebuilt-read` do Azure Document Intelligence via `requests`
- Polling simples aguarda o resultado da análise (máx. 30 tentativas, 2s cada)
- Texto extraído de todas as páginas é consolidado em uma string
- Informações estruturadas (linhas, palavras, primeiras 5 linhas) montadas e retornadas ao frontend

### Motivo
Correção do erro 404 em `POST /processar` e implementação completa da integração com o Azure.

## [Etapa 1] — 2026-04-28 — Backend retorna bounding boxes junto com o texto

### Arquivos modificados
- `app.py` — reescrito com novo formato de resposta, parâmetro `modelo` e funções separadas
- `PLANO_EVOLUCAO.md` — ETAPA 1 marcada como concluída

### O que mudou no app.py
- `chamar_document_intelligence()` agora recebe `modelo` e retorna JSON bruto (não mais apenas texto)
- Nova função `extrair_dados_do_resultado()` retorna texto + linhas com `polygon` + dimensões da página
- Rota `POST /processar` aceita parâmetro `modelo` (Form field: `read` ou `layout`, padrão `read`)
- JSON de resposta agora inclui: `texto_extraido`, `informacoes`, `pagina`, `linhas`

### Descoberta importante
- Para imagens: coordenadas em pixels (`unidade = "pixel"`)
- Para PDFs: coordenadas em inches (`unidade = "inch"`)
- Campo `pagina.unidade` já está no JSON para o frontend tratar os dois casos

### Motivo
Base obrigatória para as próximas etapas desenharem retângulos sobrepostos no preview.


### Arquivos criados
- `diagnostico.py` — script que testa automaticamente paths, versões e campos da API

### Arquivos modificados
- `app.py` — atualizado `API_VERSION` para `2024-11-30` e path para `/documentintelligence/`
- `PLANO_EVOLUCAO.md` — ETAPA 0 marcada como concluída com resultados do diagnóstico

### Resultado do diagnóstico
- Path correto: `/documentintelligence/documentModels`
- API version: `2024-11-30`
- Campo de coordenadas: `polygon` (8 valores em inches)
- Modelos disponíveis: `prebuilt-read` e `prebuilt-layout`
- `boundingBox` ausente — usar apenas `polygon`

### Motivo
Identificar a configuração exata do recurso Azure antes de implementar bounding boxes.


### Arquivos modificados
- `app.py` — corrigida URL da API: `/documentintelligence/` → `/formrecognizer/`; API version `2023-07-31` → `2022-08-31`
- `templates/index.html` — corrigida leitura do campo de erro: `dados.detalhe` → `dados.detail`

### Motivo
O recurso Azure foi criado com a versão de API anterior, que usa o path `/formrecognizer/`.
A versão `2023-07-31` com path `/documentintelligence/` retornava 404.
A mensagem de erro do backend também não aparecia na tela por leitura do campo errado.

<!-- Próximas entradas serão adicionadas aqui conforme o projeto evoluir -->
