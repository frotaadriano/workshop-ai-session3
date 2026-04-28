# Plano de Evolução — Document Intelligence com Preview e Bounding Boxes

**Projeto:** Document Intelligence + Extração Estruturada  
**Objetivo:** Evoluir a app para exibir um preview do documento com retângulos sobrepostos
nas posições exatas onde o Azure Document Intelligence extraiu cada informação.  
**Data:** 2026-04-28

---

## Visão geral do que vamos construir

```
┌─────────────────────────────────────────────────────────────────┐
│  [Selecionar documento]  [Modo: Read / Layout]  [Processar]     │
├──────────────────────────────┬──────────────────────────────────┤
│                              │  📝 Texto extraído               │
│   Preview do documento       │  ─────────────────               │
│   (imagem ou PDF renderizado)│  linha 1...                      │
│                              │  linha 2...                      │
│   ┌──────────┐               │                                  │
│   │ retângulo│ ← OCR box     │  📊 Informações estruturadas     │
│   └──────────┘               │  ─────────────────               │
│                              │  Linhas: 42                      │
│                              │  Palavras: 187                   │
└──────────────────────────────┴──────────────────────────────────┘
```

---

## Como o Azure DI retorna posições

O Azure Document Intelligence retorna, junto com cada texto extraído, um array de
coordenadas chamado `polygon` (ou `boundingBox` em versões mais antigas).

Exemplo de uma linha retornada pela API:
```json
{
  "content": "Solicitação de Exames",
  "polygon": [0.5, 0.3, 4.1, 0.3, 4.1, 0.6, 0.5, 0.6]
}
```

Os valores são pares `[x1, y1, x2, y2, x3, y3, x4, y4]` em **polegadas** (inches)
a partir do canto superior esquerdo da página.

Para desenhar retângulos na tela, precisamos:
1. Saber o tamanho real da página (também retornado pela API em `pages[].width` e `pages[].height`)
2. Renderizar o documento em um `<canvas>` HTML
3. Converter as coordenadas em polegadas para pixels no canvas

---

## Modelos disponíveis no Azure Document Intelligence

| Modelo         | Nome técnico       | O que extrai                          | Ideal para               |
|----------------|--------------------|---------------------------------------|--------------------------|
| Read           | `prebuilt-read`    | Texto + linhas + palavras + polygons  | Qualquer documento       |
| Layout         | `prebuilt-layout`  | Tudo do Read + **tabelas** + seleções | Formulários, exames      |
| Document       | `prebuilt-document`| Tudo do Layout + pares chave-valor    | Docs semi-estruturados   |
| Invoice        | `prebuilt-invoice` | Campos específicos de nota fiscal     | NFe, coupon fiscal       |
| Receipt        | `prebuilt-receipt` | Campos de recibo / comprovante        | Comprovantes             |

**Para este workshop** usaremos `prebuilt-read` e `prebuilt-layout`.

---

## Etapas do plano

---

### ETAPA 0 — Diagnóstico: validar o que o recurso Azure suporta ✅ CONCLUÍDA

**Objetivo:** Antes de codar, descobrir exatamente qual versão da API e quais modelos
estão disponíveis no recurso Azure que temos.

**Por que fazer isso?**
Recursos Azure DI criados antes de 2024 usam o path `/formrecognizer/` com API `2022-08-31`.
Recursos novos usam `/documentintelligence/` com API `2024-02-29-preview` ou `2024-11-30`.
Os campos retornados (ex: `polygon` vs `boundingBox`) variam entre as versões.

**O que será feito:**
- [x] Criar script `diagnostico.py` que testa o endpoint e descobre a versão correta
- [x] Verificar se `polygon` ou `boundingBox` está nos dados retornados
- [x] Confirmar que o modelo `prebuilt-layout` está disponível no recurso
- [x] Anotar os campos exatos que vêm na resposta (para usar nas etapas seguintes)

**Resultado do diagnóstico:**
| Item | Valor identificado |
|---|---|
| Path correto | `/documentintelligence/documentModels` |
| API version | `2024-11-30` |
| Campo de coordenadas | `polygon` (array de 8 valores em inches) |
| `prebuilt-read` disponível | ✅ sim |
| `prebuilt-layout` disponível | ✅ sim |
| Dimensões da página | `width`, `height`, `unit` em `pages[0]` |
| boundingBox | ❌ ausente — usar apenas `polygon` |

**Entregável:** saída no terminal confirmando versão, path e campos disponíveis.

---

### ETAPA 1 — Backend: retornar bounding boxes junto com o texto ✅ CONCLUÍDA

**Objetivo:** Modificar o `app.py` para retornar, além do texto, as coordenadas de
cada linha extraída — para que o frontend possa desenhar os retângulos.

**Por que fazer isso?**
Hoje o backend só retorna o texto consolidado. Para o preview funcionar, precisamos
retornar uma lista estruturada: `[{ "texto": "...", "box": [x1,y1,x2,y2] }, ...]`

**O que será feito:**
- [x] Modificar `extrair_texto_do_resultado()` para retornar lista de objetos com texto + box
- [x] Adicionar parâmetro `modelo` na rota POST (`read` ou `layout`)
- [x] Retornar também as dimensões da página (`largura_pagina`, `altura_pagina`)
- [x] Manter compatibilidade: o texto consolidado continua sendo retornado também
- [x] Tratar diferença entre `polygon` (versão nova) e `boundingBox` (versão antiga)

**Descoberta importante durante testes:**
- Para **imagens** (PNG/JPG): Azure retorna coordenadas em **pixels** e `unidade = "pixel"`
- Para **PDFs**: Azure retorna coordenadas em **inches** e `unidade = "inch"`
- O campo `pagina.unidade` já é retornado no JSON — o frontend vai precisar tratar os dois casos na ETAPA 4
- Teste com a solicitação de exame real: **58 linhas extraidas**, página 617×762 pixels

**Estrutura do JSON retornado após a etapa:**
```json
{
  "texto_extraido": "texto completo...",
  "informacoes": "resumo estruturado...",
  "pagina": { "largura": 8.5, "altura": 11.0, "unidade": "inch" },
  "linhas": [
    { "texto": "Solicitação de Exames", "box": [0.5, 0.3, 4.1, 0.6] },
    { "texto": "Paciente:", "box": [0.5, 0.8, 1.8, 1.0] }
  ]
}
```

**Entregável:** `app.py` atualizado com novo formato de resposta.

---

### ETAPA 2 — Backend: adicionar suporte ao modelo Layout ✅ CONCLUÍDA

**Objetivo:** Permitir que o usuário escolha entre `read` e `layout` no frontend,
e o backend usar o modelo correto na chamada ao Azure.

**O que é o modelo Layout?**
O `prebuilt-layout` extrai tudo que o `read` extrai, **mais**:
- Tabelas (com linhas e colunas identificadas)
- Marcadores de seleção (checkboxes marcados/desmarcados)

Para a solicitação de exame laboratorial (que tem caixinhas de seleção), o `layout`
é muito mais rico. Ele identifica quais checkboxes estão marcados.

**O que será feito:**
- [x] Receber parâmetro `modelo` no POST (`read` ou `layout`)
- [x] Usar o modelo correto na URL da chamada ao Azure
- [x] Extrair também tabelas do resultado do `layout`
- [x] Retornar tabelas no JSON: `{ "tabelas": [ { "celulas": [...] } ] }`
- [x] Extrair também seleções: `{ "selecoes": [ { "estado": "selected", "box": [...] } ] }`

**Resultado do teste com solicitação de exame (modelo layout):**
- 64 linhas de texto extraidas
- 1 tabela detectada: 25 linhas × 4 colunas (98 células)
- 47 checkboxes detectados (todos `unselected` pois o documento não tinha marcas)
- Células de tabela: texto + linha + coluna + box (polygon em pixels)
- Checkboxes: estado + box + confiança

**Entregável:** `app.py` com suporte a `read` e `layout`.

---

### ETAPA 3 — Frontend: preview do documento no browser ✅ CONCLUÍDA

**Objetivo:** Exibir o documento enviado pelo usuário na tela, antes ou durante
o processamento — como base para sobrepor os retângulos do OCR.

**Estratégia:**

#### Para imagens (PNG, JPG):
- Usar `FileReader` do JavaScript para criar uma URL local
- Exibir com uma tag `<img>` dentro de um `<div>` relativo
- Simples, sem dependências externas

#### Para PDF:
- Usar a biblioteca **PDF.js** (Mozilla), carregada via CDN
- Renderizar a **primeira página** do PDF em um elemento `<canvas>`
- PDF.js funciona 100% no browser, sem backend, sem npm

```html
<!-- CDN do PDF.js — sem instalar nada -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
```

**O que será feito:**
- [x] Detectar tipo do arquivo (imagem ou PDF) pelo `file.type`
- [x] Para imagens: exibir com `<img>` em um canvas container
- [x] Para PDF: renderizar primeira página com PDF.js em `<canvas>`
- [x] Mostrar preview logo após o upload, antes mesmo de processar
- [x] Guardar as dimensões reais do canvas renderizado (para escalar o OCR)

**Entregável:** `index.html` com preview funcional de imagem e PDF.

---

### ETAPA 4 — Frontend: desenhar retângulos sobrepostos (bounding boxes) ✅ CONCLUÍDA

**Objetivo:** Após o processamento, desenhar retângulos coloridos sobre o preview,
nas posições exatas onde o Azure DI encontrou cada linha de texto.

**Como funciona a matemática de escala:**
```
posição_pixel = (coordenada_inches / tamanho_pagina_inches) × tamanho_canvas_pixels

Exemplo:
  x_pixel = (box[0] / pagina.largura) × canvas.width
  y_pixel = (box[1] / pagina.altura)  × canvas.height
```

**O que será feito:**
- [x] Após receber o JSON com `linhas` + `pagina`, calcular o fator de escala
- [x] Para cada linha, desenhar um `strokeRect` no canvas com `2d context`
- [x] Adicionar tooltip: ao passar o mouse sobre o retângulo, mostrar o texto
- [x] Usar cores diferentes: azul para linhas de texto, laranja para seleções
- [x] Garantir que o canvas de overlay fique exatamente sobre o preview (CSS position absolute)

**Entregável:** `index.html` com retângulos sobrepostos funcionando.

---

### ETAPA 5 — Frontend: seletor de modelo e interatividade

**Objetivo:** Adicionar um seletor visual para o usuário escolher o modelo DI
e tornar a experiência mais interativa e didática para o workshop.

**O que será feito:**
- [ ] Adicionar `<select>` com opções: `Read` e `Layout`
- [ ] Enviar o modelo escolhido no FormData do POST
- [ ] Se escolher `Layout`: mostrar também as tabelas extraídas em uma seção separada
- [ ] Se escolher `Layout`: mostrar checkboxes identificados (marcados / não marcados)
- [ ] Adicionar legenda visual das cores dos retângulos
- [ ] Tornar os retângulos clicáveis: ao clicar, destaca o texto correspondente na lista

**Entregável:** Interface completa, interativa e didática.

---

### ETAPA 6 — Polimento e revisão para o workshop

**Objetivo:** Revisar tudo, garantir que funciona com os documentos de exemplo
e deixar o projeto em estado apresentável para uma gravação/demo ao vivo.

**O que será feito:**
- [ ] Testar com: imagem JPG, PDF simples, PDF com tabela, formulário de exame
- [ ] Revisar mensagens de erro (torná-las mais amigáveis)
- [ ] Adicionar comentários didáticos extras no código (para quem lê durante a gravação)
- [ ] Ajustar o README com o novo fluxo
- [ ] Atualizar o changelog com todas as etapas
- [ ] Sugestão de commits Git por etapa

---

## Resumo visual das etapas

```
ETAPA 0 → Diagnóstico do recurso Azure (script de teste)
    ↓
ETAPA 1 → Backend retorna bounding boxes no JSON
    ↓
ETAPA 2 → Backend suporta modelo Layout (tabelas + checkboxes)
    ↓
ETAPA 3 → Frontend mostra preview do documento (img/PDF)
    ↓
ETAPA 4 → Frontend desenha retângulos sobre o preview
    ↓
ETAPA 5 → Seletor de modelo + interatividade
    ↓
ETAPA 6 → Polimento final para workshop
```

---

## Ordem de execução recomendada

Execute uma etapa por vez, validando o resultado antes de avançar.
A cada etapa, o Copilot vai:
1. Mostrar exatamente o que vai mudar
2. Gerar o código da etapa
3. Explicar o que cada parte faz
4. Propor o commit Git correspondente
5. Atualizar o `changelog.md`

**Quando estiver pronto para começar, diga: "executar etapa 0"**

---

## Dependências novas que serão adicionadas

| Biblioteca | Onde usada | Forma de instalação |
|---|---|---|
| `pdf.js` | Frontend, renderizar PDF | CDN (sem instalar nada) |
| Nenhuma nova no backend | — | As atuais já são suficientes |

> Nenhuma dependência nova de Python será necessária.
> O `pdf.js` é carregado direto do CDN no HTML — zero configuração.

---

## Nota sobre versões da API e campos de bounding box

| Versão API | Path | Campo de coordenadas |
|---|---|---|
| `2022-08-31` | `/formrecognizer/` | `boundingBox` (array de 8 valores) |
| `2023-07-31`+ | `/documentintelligence/` | `polygon` (array de 8 valores) |

A etapa 0 vai identificar qual versão seu recurso usa,
e o código das etapas seguintes vai tratar os dois formatos automaticamente.
