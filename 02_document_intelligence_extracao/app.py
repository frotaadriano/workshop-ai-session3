# app.py
# Ponto de entrada da aplicação
# Demonstração didática: Document Intelligence + extração estruturada

import os
import time
import requests
from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Lê as credenciais do Azure a partir do .env
ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").rstrip("/")
KEY = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

# Versão da API do Document Intelligence
API_VERSION = "2022-08-31"

# Inicializa o app FastAPI
app = FastAPI(title="Document Intelligence Demo")

# Aponta para a pasta de templates HTML
templates = Jinja2Templates(directory="templates")


# Rota principal: exibe a interface do usuário
@app.get("/", response_class=HTMLResponse)
async def pagina_inicial(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# -------------------------------------------------------
# Rota POST /processar
# Recebe o arquivo do formulário HTML, envia para o Azure
# Document Intelligence e retorna o texto extraído.
# -------------------------------------------------------
@app.post("/processar")
async def processar_documento(arquivo: UploadFile = File(...)):

    # Valida se as credenciais estão configuradas
    if not ENDPOINT or not KEY:
        raise HTTPException(
            status_code=500,
            detail="Credenciais do Azure não configuradas. Verifique o arquivo .env."
        )

    # Lê o conteúdo do arquivo enviado pelo usuário
    conteudo_arquivo = await arquivo.read()

    # Envia o arquivo para o Azure e aguarda o resultado
    texto_extraido = chamar_document_intelligence(conteudo_arquivo, arquivo.content_type)

    # Monta as informações estruturadas a partir do texto extraído
    informacoes = montar_informacoes_estruturadas(texto_extraido)

    return JSONResponse(content={
        "texto_extraido": texto_extraido,
        "informacoes": informacoes
    })


# -------------------------------------------------------
# Função: chamar_document_intelligence
# Envia o documento para o Azure e retorna o texto extraído.
#
# Como funciona:
#   1. Faz um POST com o arquivo para iniciar a análise
#   2. O Azure retorna uma URL de status da operação
#   3. Fica consultando essa URL até o processamento terminar
#   4. Extrai e junta todo o texto encontrado nas páginas
# -------------------------------------------------------
def chamar_document_intelligence(conteudo: bytes, content_type: str) -> str:

    # URL da API para o modelo "prebuilt-read" (leitura geral de texto)
    # Usa o path /formrecognizer/ compatível com recursos criados antes de 2024
    url_analise = f"{ENDPOINT}/formrecognizer/documentModels/prebuilt-read:analyze?api-version={API_VERSION}"

    cabecalhos = {
        "Ocp-Apim-Subscription-Key": KEY,
        "Content-Type": content_type or "application/octet-stream"
    }

    # Passo 1: envia o documento para iniciar a análise
    resposta_inicial = requests.post(url_analise, headers=cabecalhos, data=conteudo)

    if resposta_inicial.status_code != 202:
        raise HTTPException(
            status_code=502,
            detail=f"Erro ao enviar documento para o Azure: {resposta_inicial.text}"
        )

    # Passo 2: pega a URL de status retornada no cabeçalho
    url_resultado = resposta_inicial.headers.get("Operation-Location")

    if not url_resultado:
        raise HTTPException(
            status_code=502,
            detail="Azure não retornou a URL de status da operação."
        )

    # Passo 3: polling — fica consultando até terminar (máx. 30 tentativas)
    cabecalhos_polling = {"Ocp-Apim-Subscription-Key": KEY}

    for _ in range(30):
        time.sleep(2)  # aguarda 2 segundos entre cada consulta
        resposta_status = requests.get(url_resultado, headers=cabecalhos_polling)
        resultado = resposta_status.json()

        status = resultado.get("status", "")

        if status == "succeeded":
            # Passo 4: extrai o texto de todas as páginas
            return extrair_texto_do_resultado(resultado)

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
# Função: extrair_texto_do_resultado
# Percorre o JSON de resposta do Azure e junta todo o texto
# encontrado nas páginas do documento.
# -------------------------------------------------------
def extrair_texto_do_resultado(resultado: dict) -> str:
    paginas = resultado.get("analyzeResult", {}).get("pages", [])

    linhas_texto = []

    for pagina in paginas:
        for linha in pagina.get("lines", []):
            linhas_texto.append(linha.get("content", ""))

    # Junta todas as linhas com quebra de linha
    return "\n".join(linhas_texto)


# -------------------------------------------------------
# Função: montar_informacoes_estruturadas
# Cria um resumo simples do texto extraído para exibir
# de forma organizada na interface.
# -------------------------------------------------------
def montar_informacoes_estruturadas(texto: str) -> str:
    if not texto:
        return "Nenhum texto encontrado no documento."

    linhas = [l for l in texto.splitlines() if l.strip()]
    palavras = texto.split()

    resumo = (
        f"Total de linhas : {len(linhas)}\n"
        f"Total de palavras: {len(palavras)}\n"
        f"Total de caracteres: {len(texto)}\n"
        f"\n--- Primeiras 5 linhas ---\n"
        + "\n".join(linhas[:5])
    )

    return resumo
