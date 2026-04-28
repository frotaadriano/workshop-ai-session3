"""
app.py — LLM + TTS Demo
========================
Fluxo:
  1. Usuário POST /processar com { "texto": "..." }
  2. Backend chama Azure OpenAI para gerar um resumo
  3. Backend chama Azure Speech TTS para converter o resumo em áudio
  4. Backend retorna { "resumo": "...", "audio_base64": "..." }
  5. Frontend exibe o resumo e toca o áudio no player HTML5
"""

import os
import base64
import html

import requests
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import AzureOpenAI

# -------------------------------------------------------
# Carrega variáveis de ambiente do arquivo .env
# -------------------------------------------------------
load_dotenv()

AZURE_OPENAI_API_KEY       = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT      = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION   = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
AZURE_OPENAI_CHAT_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o")

AZURE_SPEECH_KEY    = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION", "eastus")
AZURE_SPEECH_VOICE  = os.getenv("AZURE_SPEECH_VOICE_NAME", "pt-BR-FranciscaNeural")

# -------------------------------------------------------
# Inicializa o app FastAPI e os templates HTML
# -------------------------------------------------------
app = FastAPI(title="LLM + TTS Demo")
templates = Jinja2Templates(directory="templates")

# -------------------------------------------------------
# Modelo de dados para o corpo da requisição POST
# -------------------------------------------------------
class EntradaTexto(BaseModel):
    texto: str


# -------------------------------------------------------
# ROTA GET / — exibe a interface HTML
# -------------------------------------------------------
@app.get("/")
def pagina_inicial(request: Request):
    return templates.TemplateResponse(request, "index.html")


# -------------------------------------------------------
# FUNÇÃO: gerar_resumo
# Chama o Azure OpenAI e retorna um resumo curto do texto.
# -------------------------------------------------------
def gerar_resumo(texto: str) -> str:
    # Cria o cliente Azure OpenAI com as credenciais do .env
    cliente = AzureOpenAI(
        api_key=AZURE_OPENAI_API_KEY,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_version=AZURE_OPENAI_API_VERSION,
    )

    # Instrução para o modelo (system prompt)
    instrucao_sistema = (
        "Você é um assistente de comunicação corporativa. "
        "Sua tarefa é resumir textos de forma clara e objetiva em português do Brasil. "
        "Gere um resumo com até 5 tópicos curtos ou um parágrafo conciso. "
        "Use linguagem simples e tom profissional. "
        "Se o texto estiver vazio, muito curto ou incompreensível, diga isso explicitamente."
    )

    # Mensagem do usuário com o texto a ser resumido
    mensagem_usuario = f"Resuma o texto a seguir:\n\n{texto}"

    # Chamada ao modelo de chat
    resposta = cliente.chat.completions.create(
        model=AZURE_OPENAI_CHAT_DEPLOYMENT,
        messages=[
            {"role": "system", "content": instrucao_sistema},
            {"role": "user",   "content": mensagem_usuario},
        ],
        max_completion_tokens=1200,
        temperature=1,
    )

    # Extrai o texto do resumo da resposta
    resumo = resposta.choices[0].message.content.strip()
    return resumo


# -------------------------------------------------------
# FUNÇÃO: obter_token_speech
# Troca a chave de assinatura por um token Bearer temporário.
# O token é necessário para vozes Dragon HD na REST API.
# -------------------------------------------------------
def obter_token_speech() -> str:
    url_token = f"https://{AZURE_SPEECH_REGION}.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    resposta = requests.post(
        url_token,
        headers={"Ocp-Apim-Subscription-Key": AZURE_SPEECH_KEY},
        timeout=10,
    )
    if resposta.status_code != 200:
        raise RuntimeError(
            f"Erro ao obter token Speech (HTTP {resposta.status_code}): {resposta.text}"
        )
    return resposta.text


# -------------------------------------------------------
# FUNÇÃO: gerar_audio
# Chama a REST API do Azure Speech TTS e retorna o áudio em base64.
# -------------------------------------------------------
def gerar_audio(texto: str) -> str:
    # Obtém um token Bearer — mais confiável que a chave direta para vozes HD
    token = obter_token_speech()

    # Endpoint REST do Azure Speech TTS
    url = f"https://{AZURE_SPEECH_REGION}.tts.speech.microsoft.com/cognitiveservices/v1"

    # Cabeçalhos da requisição
    cabecalhos = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "audio-24khz-96kbitrate-mono-mp3",
    }

    # SSML: html.escape() protege contra caracteres XML no texto gerado pelo LLM
    texto_escapado = html.escape(texto)
    ssml = f"""<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="pt-BR">
  <voice name="{AZURE_SPEECH_VOICE}">
    {texto_escapado}
  </voice>
</speak>"""

    # Log no terminal do servidor para facilitar debug
    print(f"[TTS] Voz: {AZURE_SPEECH_VOICE} | Região: {AZURE_SPEECH_REGION}")
    print(f"[TTS] SSML:\n{ssml}")

    # Faz a chamada POST para a REST API
    resposta = requests.post(url, headers=cabecalhos, data=ssml.encode("utf-8"), timeout=30)

    # Log da resposta para debug
    print(f"[TTS] HTTP {resposta.status_code} | Headers: {dict(resposta.headers)}")
    if resposta.status_code != 200:
        print(f"[TTS] Corpo do erro: {resposta.text!r}")

    # Verifica se a chamada foi bem-sucedida
    if resposta.status_code != 200:
        raise RuntimeError(
            f"Erro no TTS (HTTP {resposta.status_code}): {resposta.text}"
        )

    # Converte o áudio recebido para base64
    audio_base64 = base64.b64encode(resposta.content).decode("utf-8")
    return audio_base64


# -------------------------------------------------------
# ROTA POST /processar
# Recebe o texto, gera o resumo e o áudio, retorna JSON.
# -------------------------------------------------------
@app.post("/processar")
async def processar(entrada: EntradaTexto):
    texto = entrada.texto.strip()

    # Validação básica: texto não pode estar vazio
    if not texto:
        return JSONResponse(
            status_code=400,
            content={"erro": "O texto enviado está vazio."},
        )

    try:
        # Etapa 1: gera o resumo com o Azure OpenAI
        resumo = gerar_resumo(texto)

        # Etapa 2: gera o áudio do resumo com o Azure Speech TTS
        audio_base64 = gerar_audio(resumo)

        # Retorna resumo e áudio para o frontend
        return JSONResponse(content={
            "resumo":       resumo,
            "audio_base64": audio_base64,
        })

    except Exception as ex:
        # Retorna mensagem de erro legível para o frontend
        return JSONResponse(
            status_code=500,
            content={"erro": str(ex)},
        )
