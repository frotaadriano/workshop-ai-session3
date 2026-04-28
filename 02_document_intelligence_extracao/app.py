# app.py
# Ponto de entrada da aplicação
# Demonstração didática: Document Intelligence + extração estruturada
#
# ETAPA 1: backend agora retorna, além do texto, as coordenadas (polygon)
# de cada linha extraída, e as dimensões da página — base para o preview
# com retângulos sobrepostos nas próximas etapas.

import os
import time
import requests
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Lê as credenciais do Azure a partir do .env
ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").rstrip("/")
KEY      = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

# Versão e path identificados pelo diagnostico.py
API_VERSION = "2024-11-30"
PATH_BASE   = "/documentintelligence/documentModels"

# Modelos aceitos pela API
MODELOS_VALIDOS = {"read", "layout"}

# Inicializa o app FastAPI
app = FastAPI(title="Document Intelligence Demo")

# Aponta para a pasta de templates HTML
templates = Jinja2Templates(directory="templates")


# -------------------------------------------------------
# Rota GET /
# Exibe a interface principal do usuário
# -------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def pagina_inicial(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# -------------------------------------------------------
# Rota POST /processar
# Recebe o arquivo e o modelo escolhido pelo usuário.
# Retorna JSON com:
#   - texto_extraido : texto completo em string
#   - informacoes    : resumo estruturado (linhas, palavras, etc.)
#   - pagina         : dimensões da página em inches
#   - linhas         : lista de { texto, box } para desenhar os retângulos
# -------------------------------------------------------
@app.post("/processar")
async def processar_documento(
    arquivo: UploadFile = File(...),
    modelo: str = Form("read"),        # "read" ou "layout" — padrão: read
):
    # Valida se as credenciais estão configuradas
    if not ENDPOINT or not KEY:
        raise HTTPException(
            status_code=500,
            detail="Credenciais do Azure não configuradas. Verifique o arquivo .env."
        )

    # Garante que o modelo enviado é válido
    if modelo not in MODELOS_VALIDOS:
        raise HTTPException(
            status_code=400,
            detail=f"Modelo inválido: '{modelo}'. Use 'read' ou 'layout'."
        )

    # Lê o conteúdo do arquivo enviado pelo usuário
    conteudo_arquivo = await arquivo.read()

    # Envia o arquivo para o Azure e aguarda o JSON bruto de resultado
    resultado_bruto = chamar_document_intelligence(
        conteudo_arquivo,
        arquivo.content_type,
        modelo
    )

    # Extrai do JSON: texto consolidado + linhas com boxes + dimensões da página
    texto_extraido, linhas_com_boxes, pagina = extrair_dados_do_resultado(resultado_bruto)

    # Monta o resumo textual estruturado
    informacoes = montar_informacoes_estruturadas(texto_extraido, linhas_com_boxes)

    # Retorna tudo para o frontend
    return JSONResponse(content={
        "texto_extraido": texto_extraido,
        "informacoes":    informacoes,
        "pagina":         pagina,           # { largura, altura, unidade }
        "linhas":         linhas_com_boxes, # [ { texto, box: [8 valores] }, ... ]
    })


# -------------------------------------------------------
# Função: chamar_document_intelligence
#
# Envia o documento para o Azure e devolve o JSON bruto
# da análise (analyzeResult completo).
#
# Parâmetros:
#   conteudo     : bytes do arquivo
#   content_type : mime type (application/pdf, image/png, etc.)
#   modelo       : "read" ou "layout"
#
# Como funciona:
#   1. POST com o arquivo → Azure retorna 202 + Operation-Location
#   2. GET na Operation-Location até status == "succeeded"
#   3. Devolve o JSON completo para quem chamou
# -------------------------------------------------------
def chamar_document_intelligence(conteudo: bytes, content_type: str, modelo: str) -> dict:

    url_analise = (
        f"{ENDPOINT}{PATH_BASE}"
        f"/prebuilt-{modelo}:analyze"
        f"?api-version={API_VERSION}"
    )

    cabecalhos_envio = {
        "Ocp-Apim-Subscription-Key": KEY,
        "Content-Type": content_type or "application/octet-stream",
    }

    # Passo 1: inicia a análise enviando o arquivo
    resposta_inicial = requests.post(url_analise, headers=cabecalhos_envio, data=conteudo)

    if resposta_inicial.status_code != 202:
        raise HTTPException(
            status_code=502,
            detail=f"Erro ao enviar documento para o Azure: {resposta_inicial.text}"
        )

    # Passo 2: pega a URL de polling no cabeçalho Operation-Location
    url_polling = resposta_inicial.headers.get("Operation-Location")

    if not url_polling:
        raise HTTPException(
            status_code=502,
            detail="Azure não retornou a URL de status da operação."
        )

    # Passo 3: polling — consulta a cada 2s até terminar (máx. 30 tentativas = ~60s)
    cabecalhos_polling = {"Ocp-Apim-Subscription-Key": KEY}

    for _ in range(30):
        time.sleep(2)
        resposta_status = requests.get(url_polling, headers=cabecalhos_polling)
        resultado = resposta_status.json()
        status    = resultado.get("status", "")

        if status == "succeeded":
            return resultado   # devolve o JSON bruto completo

        if status == "failed":
            raise HTTPException(
                status_code=502,
                detail="O Azure falhou ao processar o documento."
            )

    raise HTTPException(
        status_code=504,
        detail="Tempo limite excedido aguardando o processamento do Azure."
    )


# -------------------------------------------------------
# Função: extrair_dados_do_resultado
#
# Recebe o JSON bruto do Azure e extrai três coisas:
#   1. texto_consolidado : todas as linhas juntas em uma string
#   2. linhas_com_boxes  : lista de { "texto": "...", "box": [...8 valores...] }
#   3. pagina            : { "largura": 8.5, "altura": 11.0, "unidade": "inch" }
#
# O campo "box" contém o polygon do Azure:
#   [x0,y0, x1,y1, x2,y2, x3,y3] em inches, sentido horário a partir do canto sup-esq
#
# Esse formato é suficiente para o frontend calcular os retângulos no canvas.
# -------------------------------------------------------
def extrair_dados_do_resultado(resultado: dict):
    paginas = resultado.get("analyzeResult", {}).get("pages", [])

    linhas_texto    = []   # só o texto de cada linha
    linhas_com_boxes = []  # { texto, box } para o frontend

    # Informações da primeira página (usadas para escalar o canvas)
    info_pagina = {"largura": 0, "altura": 0, "unidade": "inch"}

    if paginas:
        primeira_pagina = paginas[0]
        info_pagina = {
            "largura": primeira_pagina.get("width",  0),
            "altura":  primeira_pagina.get("height", 0),
            "unidade": primeira_pagina.get("unit",   "inch"),
        }

    # Percorre todas as páginas e todas as linhas
    for pagina in paginas:
        for linha in pagina.get("lines", []):
            texto   = linha.get("content", "")
            polygon = linha.get("polygon", [])  # 8 valores em inches

            linhas_texto.append(texto)

            linhas_com_boxes.append({
                "texto": texto,
                "box":   polygon,   # [x0,y0,x1,y1,x2,y2,x3,y3]
            })

    texto_consolidado = "\n".join(linhas_texto)

    return texto_consolidado, linhas_com_boxes, info_pagina


# -------------------------------------------------------
# Função: montar_informacoes_estruturadas
#
# Gera um resumo textual simples para exibir na interface:
# quantidade de linhas, palavras, caracteres e primeiras linhas.
# -------------------------------------------------------
def montar_informacoes_estruturadas(texto: str, linhas: list) -> str:
    if not texto:
        return "Nenhum texto encontrado no documento."

    palavras = texto.split()

    resumo = (
        f"Total de linhas     : {len(linhas)}\n"
        f"Total de palavras   : {len(palavras)}\n"
        f"Total de caracteres : {len(texto)}\n"
        f"\n--- Primeiras 5 linhas ---\n"
        + "\n".join(l["texto"] for l in linhas[:5])
    )

    return resumo
