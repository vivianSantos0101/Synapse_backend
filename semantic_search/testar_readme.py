import httpx
import sys

arquivo = sys.argv[1] if len(sys.argv) > 1 else "README.md"
repo_name = sys.argv[2] if len(sys.argv) > 2 else "empresa/teste"

with open(arquivo, "r", encoding="utf-8") as f:
    conteudo = f.read()

BASE_URL = "http://localhost:8000/api/v1"

# Timeout generoso: o modelo de embedding pode ser lento na primeira chamada.
TIMEOUT = httpx.Timeout(connect=10.0, read=120.0, write=10.0, pool=10.0)

# ── Indexação ──────────────────────────────────────────────────────────────────
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

# ── Busca ──────────────────────────────────────────────────────────────────────
query = input("\nDigite sua busca: ").strip()
if not query:
    print("[ERRO] Busca vazia.")
    sys.exit(1)

# Chamada de diagnóstico: sem filtro para ver todos os scores brutos
print("\n[DIAGNÓSTICO] Scores brutos (sem filtro):")
try:
    resp_raw = httpx.post(
        f"{BASE_URL}/search",
        json={"query": query, "top_k": 10, "min_score": 0.0},
        timeout=TIMEOUT,
    )
    resp_raw.raise_for_status()
    data_raw = resp_raw.json()

    print(f"  {'':2} {'REPO':<25} {'SEÇÃO':<30} {'SCORE':>7}")
    print(f"  {'':2} {'-'*25} {'-'*30} {'-'*7}")
    for r in data_raw["results"]:
        secao = r.get("section") or "(sem seção)"
        repo = r.get("repo_name", "(sem repo)")
        score = r.get("score", 0.0)
        marcador = "✓" if score >= 0.30 else "✗"
        print(f"  {marcador}  {repo:<25} {secao:<30} {score:>7.4f}")
    print()

except httpx.TimeoutException:
    print("[ERRO] Timeout na busca de diagnóstico.")
    sys.exit(1)
except Exception as e:
    print(f"[ERRO] Falha no diagnóstico: {e}")

# Busca real com filtro
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

# ── Resultado ─────────────────────────────────────────────────────────────────
try:
    data = resp.json()
except Exception:
    print(f"[ERRO] Resposta inválida do servidor:\n{resp.text}")
    sys.exit(1)

total = data.get("total_results", 0)
print(f"Resultados encontrados (min_score=0.30): {total}")

if total == 0:
    print("  Nenhum chunk passou o threshold.")
    print("  Veja o diagnóstico acima para entender os scores reais.")
else:
    for r in data["results"]:
        secao = r.get("section") or "(sem seção)"
        print(f"\n  Repo:    {r.get('repo_name', '')}")
        print(f"  Seção:   {secao}")
        print(f"  Score:   {r.get('score', 0.0)}")
        print(f"  Trecho:  {r.get('excerpt', '')[:200]}")