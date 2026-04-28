"""
app.py — AI Search + Mini RAG
Demonstração didática de um fluxo RAG para workshop de introdução à IA.

Fluxo:
  1. Usuário faz uma pergunta
  2. Backend busca trechos relevantes no Azure AI Search
  3. Backend monta um prompt com o contexto recuperado
  4. Backend chama o Azure OpenAI para gerar a resposta final
  5. Resposta, trechos e pergunta são exibidos na interface
"""

import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from openai import AzureOpenAI

# Carrega as variáveis do arquivo .env
load_dotenv()

# -------------------------------------------------------
# Configurações do Azure AI Search
# -------------------------------------------------------
SEARCH_ENDPOINT = os.getenv("AZURE_SEARCH_ENDPOINT")
SEARCH_KEY = os.getenv("AZURE_SEARCH_KEY")
SEARCH_INDEX = os.getenv("AZURE_SEARCH_INDEX_NAME")

# Nomes dos campos no índice (ajuste no .env se os seus campos tiverem outro nome)
CAMPO_CONTEUDO = os.getenv("AZURE_SEARCH_CONTENT_FIELD", "content")
CAMPO_TITULO = os.getenv("AZURE_SEARCH_TITLE_FIELD", "title")

# -------------------------------------------------------
# Configurações do Azure OpenAI
# -------------------------------------------------------
OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

# Inicializa o cliente do Azure OpenAI
cliente_openai = AzureOpenAI(
    api_key=OPENAI_API_KEY,
    azure_endpoint=OPENAI_ENDPOINT,
    api_version=OPENAI_API_VERSION
)

# -------------------------------------------------------
# Inicializa o FastAPI e os templates HTML
# -------------------------------------------------------
app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Modelo de entrada: o que o frontend vai enviar
class PerguntaRequest(BaseModel):
    pergunta: str


# -------------------------------------------------------
# FUNÇÃO 1: Buscar trechos relevantes no Azure AI Search
# -------------------------------------------------------
def buscar_trechos_relevantes(pergunta: str, quantidade: int = 3) -> list[dict]:
    """
    Envia a pergunta ao Azure AI Search e retorna os trechos mais relevantes.

    O Azure AI Search recebe o texto da pergunta e devolve os documentos
    que mais se aproximam semanticamente ou por palavras-chave.

    Parâmetros:
        pergunta   : texto da pergunta do usuário
        quantidade : número máximo de trechos a retornar (padrão: 3)

    Retorno:
        Lista de dicionários com 'titulo' e 'conteudo' de cada trecho.
    """
    # Monta a URL da API REST do Azure AI Search
    url = f"{SEARCH_ENDPOINT}/indexes/{SEARCH_INDEX}/docs/search?api-version=2023-11-01"

    # Cabeçalhos da requisição: autenticação por chave de API
    cabecalhos = {
        "Content-Type": "application/json",
        "api-key": SEARCH_KEY
    }

    # Corpo da busca: texto da pergunta, quantos resultados e quais campos retornar
    corpo_da_busca = {
        "search": pergunta,
        "top": quantidade,
        "select": f"{CAMPO_TITULO},{CAMPO_CONTEUDO}"
    }

    # Faz a requisição ao Azure AI Search
    resposta = requests.post(url, headers=cabecalhos, json=corpo_da_busca, timeout=10)
    resposta.raise_for_status()

    # Extrai os documentos da resposta
    resultados = resposta.json().get("value", [])

    # Monta a lista de trechos com os campos que nos interessam
    trechos = []
    for item in resultados:
        trechos.append({
            "titulo": item.get(CAMPO_TITULO, "Sem título"),
            "conteudo": item.get(CAMPO_CONTEUDO, ""),
            "score": round(item.get("@search.score", 0), 2)  # score de relevância retornado pelo AI Search
        })

    return trechos


# -------------------------------------------------------
# FUNÇÃO 2: Montar o prompt com o contexto recuperado
# -------------------------------------------------------
def montar_prompt_com_contexto(pergunta: str, trechos: list[dict]) -> str:
    """
    Monta o prompt que será enviado ao Azure OpenAI.

    O prompt inclui:
      - instrução de comportamento do assistente
      - os trechos recuperados como contexto
      - a pergunta do usuário

    Este é o coração do RAG: o LLM recebe contexto real antes de responder.
    """
    # Concatena os trechos em um bloco de texto legível
    bloco_contexto = ""
    for i, trecho in enumerate(trechos, start=1):
        bloco_contexto += f"\n[Trecho {i}] {trecho['titulo']}\n{trecho['conteudo']}\n"

    # Monta o prompt completo
    prompt = f"""Você é um assistente corporativo prestativo.
Responda à pergunta usando prioritariamente o contexto fornecido abaixo.
Se a resposta não estiver suficientemente sustentada pelo contexto, diga isso explicitamente.
Use linguagem clara, objetiva e em português do Brasil.

--- CONTEXTO RECUPERADO ---
{bloco_contexto}
--- FIM DO CONTEXTO ---

Pergunta: {pergunta}
Resposta:"""

    return prompt


# -------------------------------------------------------
# FUNÇÃO 3: Gerar a resposta final com Azure OpenAI
# -------------------------------------------------------
def gerar_resposta_final(prompt: str) -> str:
    """
    Envia o prompt ao Azure OpenAI e retorna a resposta gerada pelo modelo.

    O modelo recebe o contexto recuperado e a pergunta juntos,
    e gera uma resposta baseada nesse contexto.
    """
    resposta = cliente_openai.chat.completions.create(
        model=OPENAI_DEPLOYMENT,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=1,  
        max_completion_tokens=1000
    )

    return resposta.choices[0].message.content.strip()


# -------------------------------------------------------
# ROTA: Página inicial — exibe a interface HTML
# -------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def pagina_inicial(request: Request):
    return templates.TemplateResponse(request, "index.html")


# -------------------------------------------------------
# ROTA: Receber pergunta e executar o fluxo RAG completo
# -------------------------------------------------------
@app.post("/perguntar")
async def perguntar(dados: PerguntaRequest):
    """
    Orquestra o fluxo RAG em 3 passos:
      1. Busca trechos relevantes no Azure AI Search
      2. Monta o prompt com o contexto recuperado
      3. Gera a resposta final com o Azure OpenAI

    Retorna para o frontend:
      - a pergunta enviada
      - os trechos encontrados
      - um resumo do prompt montado
      - a resposta final gerada pelo LLM
    """
    pergunta = dados.pergunta.strip()

    # Validação básica
    if not pergunta:
        return JSONResponse(
            content={"erro": "A pergunta não pode estar vazia."},
            status_code=400
        )

    try:
        # PASSO 1 — Buscar trechos relevantes
        trechos = buscar_trechos_relevantes(pergunta)

        # PASSO 2 — Montar o prompt com contexto
        prompt = montar_prompt_com_contexto(pergunta, trechos)

        # PASSO 3 — Gerar a resposta final
        resposta = gerar_resposta_final(prompt)

        # Retorna tudo para a interface
        return {
            "pergunta": pergunta,
            "trechos": trechos,
            "prompt_resumido": prompt[:600] + "\n..." if len(prompt) > 600 else prompt,
            "resposta": resposta
        }

    except requests.HTTPError as erro:
        # Erro ao chamar o Azure AI Search
        return JSONResponse(
            content={"erro": f"Erro na busca (Azure AI Search): {str(erro)}"},
            status_code=500
        )
    except Exception as erro:
        # Qualquer outro erro inesperado
        return JSONResponse(
            content={"erro": f"Erro inesperado: {str(erro)}"},
            status_code=500
        )
