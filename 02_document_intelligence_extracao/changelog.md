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

## [Etapa 5] — 2026-04-28 — Frontend: cards de tabela, checkboxes e interatividade

### Arquivos modificados
- `templates/index.html` — novos cards, funções JS e interação clique
- `PLANO_EVOLUCAO.md` — ETAPA 5 marcada como concluída

### O que mudou
- Novo card `#card-selecoes`: lista todos os checkboxes com estado (☑/☐) e % de confiança
- Novo card `#card-tabelas`: renderiza a tabela extraída como `<table>` HTML legível
  - Células do DI com `:unselected:` e `:selected:` são trocadas por ☐/☑
  - Primeira linha vira cabeçalho `<th>`; demais viram `<td>`
- `mostrarSelecoes()`: renderiza lista de checkboxes com `data-idx` para destaque
- `mostrarTabela()`: reconstrói a grade 2D a partir da lista plana de células
- `esconderCards()` atualizada: limpa também `card-selecoes` e `card-tabelas`
- Clique no overlay: destaca visualmente o item correspondente na lista de checkboxes
  e rola a lista até ele (`.linha-destacada` com timeout de 2s)
- `idx` adicionado nas áreas de seleção do `configurarTooltip()` para o hit-test de clique

### Motivo
Tornar a demo mais rica e didática: o workshop pode mostrar a relação visual entre
 o retângulo no documento e o item correspondente na lista extraída.


### Arquivos modificados
- `templates/index.html` — adicionadas funções `desenharRetangulos()` e `configurarTooltip()`
- `PLANO_EVOLUCAO.md` — ETAPA 4 marcada como concluída

### O que mudou
- `desenharRetangulos(linhas, pagina, selecoes)`: chamada após o processamento
  - Redimensiona `#canvas-overlay` para o tamanho real do container na tela
  - Calcula `fatorX/fatorY` (coordenada DI → pixel do overlay)
  - Linhas de texto: retângulo azul `rgba(26,115,232)`
  - Checkboxes: laranja translúcido (sólido se `selected`)
- `configurarTooltip()`: ao mover o mouse sobre o overlay, faz hit-test e exibe o texto no tooltip
- `#ocr-tooltip`: div flutuante com `position:fixed` para o tooltip
- Legenda de cores exibida abaixo do preview após processar
- `pointer-events: auto` no overlay para capturar eventos de mouse

### Motivo
Efeito visual principal do workshop: ver exatamente onde o Azure DI identificou cada texto.


### Arquivos modificados
- `templates/index.html` — reescrito com layout dois-painéis e lógica de preview
- `PLANO_EVOLUCAO.md` — ETAPA 3 marcada como concluída

### O que mudou
- Layout dois-painéis: preview à esquerda (480px), resultados à direita
- Seletor de modelo adicionado ao formulário (`read` ou `layout`)
- `renderizarPreviewPDF()`: usa PDF.js (CDN) para renderizar PDF no `<canvas>`
- `renderizarPreviewImagem()`: usa FileReader + `<img>` para PNG/JPG
- Preview exibido imediatamente após o upload, antes do processamento
- `dimensoesCanvas` armazenado globalmente para uso na ETAPA 4
- `#canvas-overlay` adicionado (position:absolute sobre o preview) — pronto para ETAPA 4
- FormData agora envia também o campo `modelo`

### Motivo
Base visual para sobrepor retângulos OCR na ETAPA 4. Sem o preview, não há onde desenhar.


### Arquivos modificados
- `app.py` — adicionadas funções `extrair_tabelas()` e `extrair_selecoes()`, resposta da rota atualizada
- `PLANO_EVOLUCAO.md` — ETAPA 2 marcada como concluída

### O que mudou no app.py
- Nova função `extrair_tabelas()`: percorre `analyzeResult.tables`, extrai células com texto + posição (linha/coluna) + polygon
- Nova função `extrair_selecoes()`: percorre `pages[].selectionMarks`, extrai estado (`selected`/`unselected`) + polygon + confiança
- `montar_informacoes_estruturadas()` atualizada: exibe contagem de tabelas e checkboxes quando presentes
- JSON de resposta agora inclui: `tabelas` e `selecoes` (vazios quando modelo=read)

### Resultado do teste
- Modelo layout + solicitação de exame: 1 tabela (25×4), 47 checkboxes detectados

### Motivo
Permite que o frontend desenhe retangulos diferenciados para texto, celulas de tabela e checkboxes nas próximas etapas.


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
