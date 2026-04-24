# app.py — STT + Resumo com LLM
# Aplicação demo de workshop: captura áudio, transcreve e gera resumo com IA.

import os
import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from openai import AzureOpenAI
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configurações do Azure Speech to Text ---
SPEECH_KEY    = os.getenv("AZURE_SPEECH_KEY")
SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")

# --- Configurações do Azure OpenAI ---
OPENAI_API_KEY    = os.getenv("AZURE_OPENAI_API_KEY")
OPENAI_ENDPOINT   = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")
OPENAI_DEPLOYMENT  = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

# --- Inicialização do app e templates ---
app = FastAPI(title="STT + Resumo com LLM")
templates = Jinja2Templates(directory="templates")


# =============================================================
# ROTA: Página principal
# =============================================================

@app.get("/", response_class=HTMLResponse)
async def pagina_inicial(request: Request):
    """Serve a página HTML principal da aplicação."""
    return templates.TemplateResponse(request, "index.html")


# =============================================================
# ROTA: Processamento do áudio
# =============================================================

@app.post("/processar")
async def processar_audio(audio: UploadFile = File(...)):
    """
    Recebe o arquivo WAV gravado pelo navegador,
    chama o Azure Speech to Text para transcrever,
    e em seguida chama o Azure OpenAI para gerar o resumo.
    """
    try:
        # Lê o conteúdo binário do arquivo enviado
        conteudo_audio = await audio.read()
        tamanho_kb = len(conteudo_audio) / 1024

        # Valida que o áudio não está vazio
        if len(conteudo_audio) < 1000:
            return {"erro": f"Áudio muito pequeno ({tamanho_kb:.1f} KB). A gravação pode ter falhado."}

        # Usa o content_type real enviado pelo frontend (audio/wav)
        tipo_audio = audio.content_type or "audio/wav"

        # Etapa 1: Transcrever o áudio
        transcricao = transcrever_audio(conteudo_audio, tipo_audio)

        # Se a transcrição vier vazia, avisa o usuário
        if not transcricao:
            return {
                "transcricao": "(nenhum texto detectado)",
                "resumo": "Não foi possível transcrever o áudio. Tente falar mais perto do microfone e de forma clara."
            }

        # Etapa 2: Gerar o resumo com Azure OpenAI
        resumo = gerar_resumo(transcricao)

        return {"transcricao": transcricao, "resumo": resumo}

    except Exception as erro:
        # Retorna o erro de forma legível para facilitar o diagnóstico
        return {"erro": f"Erro ao processar o áudio: {str(erro)}"}


# =============================================================
# FUNÇÃO: Transcrição com Azure Speech to Text (REST)
# =============================================================

def transcrever_audio(conteudo_audio: bytes, tipo_audio: str = "audio/wav") -> str:
    """
    Envia o áudio WAV para a API REST do Azure Speech to Text
    e retorna o texto transcrito.

    O frontend converte o áudio para WAV PCM 16kHz (formato garantido pela Azure).
    """
    # URL da API de reconhecimento de fala
    url = (
        f"https://{SPEECH_REGION}.stt.speech.microsoft.com"
        f"/speech/recognition/conversation/cognitiveservices/v1"
    )

    # Cabeçalhos: chave de autenticação e formato do áudio
    cabecalhos = {
        "Ocp-Apim-Subscription-Key": SPEECH_KEY,
        "Content-Type": tipo_audio,
    }

    # Parâmetro: idioma esperado na transcrição
    parametros = {
        "language": "pt-BR",
    }

    # Faz a chamada para o serviço de Speech to Text
    resposta = requests.post(
        url,
        headers=cabecalhos,
        params=parametros,
        data=conteudo_audio,
        timeout=30
    )

    # Interpreta o JSON de resposta
    dados = resposta.json()

    # Verifica o status do reconhecimento
    status = dados.get("RecognitionStatus", "")
    if status not in ("Success", ""):
        # Status como "Silence" ou "InitialSilenceTimeout" indicam áudio sem fala
        return ""

    # "DisplayText" contém o texto transcrito (já formatado)
    return dados.get("DisplayText", "")


# =============================================================
# FUNÇÃO: Geração de resumo com Azure OpenAI
# =============================================================

def gerar_resumo(transcricao: str) -> str:
    """
    Envia a transcrição para o Azure OpenAI
    e retorna um resumo em 3 a 5 tópicos curtos.
    """
    # Inicializa o cliente com as configurações do Azure OpenAI
    cliente = AzureOpenAI(
        api_key=OPENAI_API_KEY,
        azure_endpoint=OPENAI_ENDPOINT,
        api_version=OPENAI_API_VERSION,
    )

    # Instrução de comportamento para o modelo
    instrucao_sistema = (
        "Você é um assistente que resume textos de forma clara e objetiva. "
        "Resuma a transcrição em 3 a 5 tópicos curtos, em português do Brasil, "
        "com linguagem clara e objetiva. "
        "Se a transcrição estiver incompleta ou pouco compreensível, diga isso explicitamente."
    )

    # Chama o modelo de chat com a transcrição
    resposta = cliente.chat.completions.create(
        model=OPENAI_DEPLOYMENT,
        messages=[
            {"role": "system", "content": instrucao_sistema},
            {"role": "user", "content": f"Transcrição:\n{transcricao}"},
        ],
        max_completion_tokens=300,
        temperature=1, 
    )

    # Extrai e retorna o texto do resumo gerado
    return resposta.choices[0].message.content
