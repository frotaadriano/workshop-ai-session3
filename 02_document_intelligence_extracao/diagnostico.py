# diagnostico.py
# Script de diagnóstico do recurso Azure Document Intelligence
#
# Execute com:  python diagnostico.py
#
# O script testa automaticamente quais versões da API e paths funcionam
# no seu recurso, e mostra os campos disponíveis na resposta.
# Isso é necessário porque recursos criados antes/depois de 2024
# usam paths e campos diferentes.

import os
import time
import json
import requests
from dotenv import load_dotenv

# Carrega as credenciais do .env
load_dotenv()

ENDPOINT = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT", "").rstrip("/")
KEY      = os.getenv("AZURE_DOCUMENT_INTELLIGENCE_KEY", "")

# PDF mínimo válido de 1 página em branco (base64-decodificado)
# Usado apenas para testar a conexão - não precisa de conteúdo real
PDF_MINIMO = (
    b"%PDF-1.4\n"
    b"1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n"
    b"2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n"
    b"3 0 obj<</Type/Page/MediaBox[0 0 612 792]/Parent 2 0 R"
    b"/Contents 4 0 R/Resources<</Font<</F1 5 0 R>>>>>>endobj\n"
    b"4 0 obj<</Length 44>>stream\nBT /F1 12 Tf 100 700 Td (Teste) Tj ET\nendstream\nendobj\n"
    b"5 0 obj<</Type/Font/Subtype/Type1/BaseFont/Helvetica>>endobj\n"
    b"xref\n0 6\n0000000000 65535 f\n"
    b"0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\n"
    b"0000000266 00000 n\n0000000360 00000 n\n"
    b"trailer<</Size 6/Root 1 0 R>>\nstartxref\n441\n%%EOF"
)

# -------------------------------------------------------
# Combinações a testar: path + versão da API + modelos
# -------------------------------------------------------
COMBINACOES = [
    {
        "rotulo":      "NOVO  — /documentintelligence/ + 2024-11-30",
        "path_base":   "/documentintelligence/documentModels",
        "api_version": "2024-11-30",
    },
    {
        "rotulo":      "NOVO  — /documentintelligence/ + 2024-02-29-preview",
        "path_base":   "/documentintelligence/documentModels",
        "api_version": "2024-02-29-preview",
    },
    {
        "rotulo":      "MEDIO — /documentintelligence/ + 2023-07-31",
        "path_base":   "/documentintelligence/documentModels",
        "api_version": "2023-07-31",
    },
    {
        "rotulo":      "ANTIGO — /formrecognizer/ + 2022-08-31",
        "path_base":   "/formrecognizer/documentModels",
        "api_version": "2022-08-31",
    },
    {
        "rotulo":      "ANTIGO — /formrecognizer/ + 2022-06-30-preview",
        "path_base":   "/formrecognizer/documentModels",
        "api_version": "2022-06-30-preview",
    },
]

MODELOS = ["prebuilt-read", "prebuilt-layout"]

# -------------------------------------------------------
# Funções auxiliares
# -------------------------------------------------------

def separador(char="─", largura=60):
    print(char * largura)

def secao(titulo):
    separador("═")
    print(f"  {titulo}")
    separador("═")

def subsecao(titulo):
    separador()
    print(f"  {titulo}")
    separador()


def testar_combinacao(combinacao, modelo):
    """
    Envia o PDF mínimo para a API com a combinação de path + versão + modelo.
    Retorna (sucesso, status_code, url, resultado_json_ou_erro)
    """
    url = (
        f"{ENDPOINT}{combinacao['path_base']}"
        f"/{modelo}:analyze"
        f"?api-version={combinacao['api_version']}"
    )

    cabecalhos = {
        "Ocp-Apim-Subscription-Key": KEY,
        "Content-Type": "application/pdf",
    }

    try:
        # Passo 1: inicia a análise
        resp = requests.post(url, headers=cabecalhos, data=PDF_MINIMO, timeout=15)

        if resp.status_code != 202:
            return False, resp.status_code, url, resp.text[:300]

        # Passo 2: pega a URL de polling
        url_polling = resp.headers.get("Operation-Location", "")
        if not url_polling:
            return False, 202, url, "202 recebido mas sem Operation-Location no cabeçalho"

        # Passo 3: polling até terminar (máx. 20s)
        cabecalho_poll = {"Ocp-Apim-Subscription-Key": KEY}
        for _ in range(10):
            time.sleep(2)
            r = requests.get(url_polling, headers=cabecalho_poll, timeout=15)
            dados = r.json()
            status = dados.get("status", "")
            if status == "succeeded":
                return True, 200, url, dados
            if status == "failed":
                return False, 200, url, f"Análise falhou: {json.dumps(dados)[:300]}"

        return False, 0, url, "Timeout: análise não completou em 20s"

    except requests.exceptions.RequestException as e:
        return False, -1, url, str(e)


def inspecionar_campos(resultado):
    """
    Inspeciona o JSON retornado pela API e mostra quais campos
    de coordenadas estão disponíveis (polygon vs boundingBox).
    """
    analyze = resultado.get("analyzeResult", {})
    paginas = analyze.get("pages", [])

    if not paginas:
        print("    ⚠️  Nenhuma página encontrada no resultado.")
        return

    pagina = paginas[0]
    print(f"    📄 Dimensões da página:")
    print(f"       width  = {pagina.get('width', 'N/A')}")
    print(f"       height = {pagina.get('height', 'N/A')}")
    print(f"       unit   = {pagina.get('unit', 'N/A')}")

    linhas = pagina.get("lines", [])
    palavras = pagina.get("words", [])

    print(f"\n    📝 Linhas retornadas : {len(linhas)}")
    print(f"    🔤 Palavras retornadas: {len(palavras)}")

    # Verifica campos de coordenadas
    if linhas:
        linha = linhas[0]
        print(f"\n    🔍 Campos da primeira linha:")
        for campo in ["content", "polygon", "boundingBox", "spans"]:
            valor = linha.get(campo)
            if valor is not None:
                print(f"       ✅ '{campo}' presente → {str(valor)[:80]}")
            else:
                print(f"       ❌ '{campo}' ausente")

    if palavras:
        palavra = palavras[0]
        print(f"\n    🔍 Campos da primeira palavra:")
        for campo in ["content", "polygon", "boundingBox", "confidence"]:
            valor = palavra.get(campo)
            if valor is not None:
                print(f"       ✅ '{campo}' presente → {str(valor)[:80]}")
            else:
                print(f"       ❌ '{campo}' ausente")

    # Verifica se tem tabelas (layout)
    tabelas = analyze.get("tables", [])
    print(f"\n    📊 Tabelas retornadas: {len(tabelas)}")

    # Verifica se tem selection marks
    selecoes = []
    for p in paginas:
        selecoes += p.get("selectionMarks", [])
    print(f"    ☑️  Marcadores de seleção: {len(selecoes)}")


# -------------------------------------------------------
# Main — executa o diagnóstico completo
# -------------------------------------------------------

def main():
    secao("DIAGNÓSTICO — Azure Document Intelligence")

    if not ENDPOINT or not KEY:
        print("\n❌ ERRO: Credenciais não encontradas no .env")
        print("   Configure AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT e AZURE_DOCUMENT_INTELLIGENCE_KEY")
        return

    print(f"\n  Endpoint: {ENDPOINT}")
    print(f"  Chave   : {KEY[:8]}{'*' * (len(KEY) - 8)}")
    print()

    # ─── Fase 1: detectar combinação de path + versão ───────────────────────
    secao("FASE 1 — Testando paths e versões da API")

    combinacao_ok = None

    for combinacao in COMBINACOES:
        for modelo in MODELOS:
            rotulo = f"{combinacao['rotulo']} | modelo: {modelo}"
            print(f"\n  Testando: {rotulo}")
            print(f"  Aguardando resposta do Azure...", end=" ", flush=True)

            sucesso, code, url, resultado = testar_combinacao(combinacao, modelo)

            if sucesso:
                print("✅ FUNCIONOU!")
                print(f"  URL: {url}")

                if combinacao_ok is None:
                    combinacao_ok = {**combinacao, "modelo_testado": modelo}

                subsecao(f"Inspecionando campos retornados — {modelo}")
                inspecionar_campos(resultado)
                print()
            else:
                print(f"❌ Falhou (HTTP {code})")
                if code not in (404, 400):
                    print(f"  Detalhe: {str(resultado)[:200]}")

    # ─── Fase 2: resumo final ────────────────────────────────────────────────
    secao("FASE 2 — Resumo do Diagnóstico")

    if combinacao_ok:
        print(f"""
  ✅ Recurso Azure funcionando!

  ┌─────────────────────────────────────────────────────┐
  │  Configuração identificada:                         │
  │                                                     │
  │  Path base  : {combinacao_ok['path_base']:<38}│
  │  API version: {combinacao_ok['api_version']:<38}│
  └─────────────────────────────────────────────────────┘

  O que atualizar no app.py:
    API_VERSION = "{combinacao_ok['api_version']}"
    # path: {combinacao_ok['path_base']}
""")
    else:
        print("""
  ❌ Nenhuma combinação funcionou.

  Possíveis causas:
  1. Credenciais incorretas no .env
  2. Recurso Azure desativado ou sem saldo
  3. Endpoint com erro de digitação
  4. Firewall ou rede bloqueando o acesso

  Verifique no Portal Azure:
  → https://portal.azure.com
  → Cognitive Services > seu recurso > Keys and Endpoint
""")

    separador("═")
    print("  Diagnóstico concluído.")
    separador("═")


if __name__ == "__main__":
    main()
