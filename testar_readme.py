import httpx
import sys

arquivo = sys.argv[1] if len(sys.argv) > 1 else "README.md"
repo_name = sys.argv[2] if len(sys.argv) > 2 else "empresa/teste"

with open(arquivo, "r", encoding="utf-8") as f:
    conteudo = f.read()

BASE_URL = "http://localhost:8000/api/v1"
TIMEOUT = httpx.Timeout(connect=10.0, read=120.0, write=10.0, pool=10.0)

print(f"Indexando '{repo_name}'...")
try:
    resp = httpx.post(
        f"{BASE_URL}/index",
        json={"repo_name": repo_name, "content": conteudo, "metadata": {"arquivo": arquivo}},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
    print(resp.json())
except httpx.TimeoutException:
    print("[ERRO] Timeout na indexação — o servidor demorou demais para responder.")
    sys.exit(1)
except httpx.HTTPStatusError as e:
    print(f"[ERRO] HTTP {e.response.status_code}: {e.response.text}")
    sys.exit(1)

query = input("\nDigite sua busca: ").strip()
if not query:
    print("[ERRO] Busca vazia.")
    sys.exit(1)

print("\nBuscando na base de dados da empresa...")
try:
    resp = httpx.post(
        f"{BASE_URL}/search",
        json={"query": query, "top_k": 5, "min_score": 0.30},
        timeout=TIMEOUT,
    )
    resp.raise_for_status()
except httpx.TimeoutException:
    print("[ERRO] Timeout na busca — tente novamente.")
    sys.exit(1)
except httpx.HTTPStatusError as e:
    print(f"[ERRO] HTTP {e.response.status_code}: {e.response.text}")
    sys.exit(1)

try:
    data = resp.json()
except Exception:
    print(f"[ERRO] Resposta inválida do servidor:\n{resp.text}")
    sys.exit(1)

total = data.get("total_results", 0)

if total == 0:
    print(f" Nenhum resultado relevante encontrado para '{query}'.")
else:
    print(f" Encontrado em {total} lugar(es) (Score mínimo atingido)\n")
    print("-" * 60)
    
    for i, r in enumerate(data.get("results", []), 1):
        repo = r.get("repo_name", "Desconhecido")
        score = r.get("score", 0.0)
        excerpt = r.get("excerpt", "")[:250].replace("\n", " ")
        
        print(f"RESULTADO {i} | Repo: {repo} | Score: {score:.4f}")
        print(f"Trecho: {excerpt}...\n")
        print("-" * 60)