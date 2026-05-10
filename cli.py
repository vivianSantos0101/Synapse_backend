"""
CLI — Synapse Semantic Search
Indexa READMEs e busca projetos existentes via pgvector.

Uso:
    python cli.py index --dir readmes/
    python cli.py index --file README.md --repo empresa/proj
    python cli.py search "autenticação OAuth"
    python cli.py stats
"""

import argparse
import os
import sys
import time

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.init_db import init_db
from app.services.chunker import chunk_readme
from app.services.embedding_service import get_embedding_service
from app.services.vector_store import get_vector_store

console = Console()


def _repo_name_from_filename(filepath: str) -> str:
    base = os.path.splitext(os.path.basename(filepath))[0]
    return f"empresa/{base}"


def _read_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def cmd_index(args: argparse.Namespace) -> None:
    init_db()
    embedder = get_embedding_service()
    store = get_vector_store()

    files: list[tuple[str, str]] = []

    if args.file:
        repo = args.repo or _repo_name_from_filename(args.file)
        files.append((args.file, repo))
    elif args.dir:
        for fname in sorted(os.listdir(args.dir)):
            if fname.endswith(".md"):
                fpath = os.path.join(args.dir, fname)
                files.append((fpath, _repo_name_from_filename(fpath)))
    else:
        console.print("[red]Erro:[/] informe --file ou --dir.")
        sys.exit(1)

    if not files:
        console.print("[yellow]Nenhum arquivo .md encontrado.[/]")
        return

    table = Table(title="Indexação de READMEs", show_lines=True)
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Repositório", style="cyan")
    table.add_column("Chunks", justify="right", style="green")
    table.add_column("Tempo", justify="right", style="yellow")

    total_chunks = 0

    for i, (fpath, repo) in enumerate(files, 1):
        t0 = time.perf_counter()
        content = _read_file(fpath)

        store.delete_repo(repo)
        chunks = chunk_readme(content, repo)

        if not chunks:
            table.add_row(str(i), repo, "0", "—")
            continue

        embeddings = embedder.embed([c["text"] for c in chunks])
        count = store.upsert_chunks(chunks, embeddings)
        elapsed = time.perf_counter() - t0

        total_chunks += count
        table.add_row(str(i), repo, str(count), f"{elapsed:.2f}s")

    console.print()
    console.print(table)
    console.print(f"\n[bold green]OK[/] {len(files)} repositorios indexados -- {total_chunks} chunks no total.\n")


def cmd_search(args: argparse.Namespace) -> None:
    init_db()
    embedder = get_embedding_service()
    store = get_vector_store()

    query = args.query
    top_k = args.top_k
    min_score = args.min_score

    console.print(f"\n[bold]Buscando:[/] [italic]{query}[/]\n")

    query_embedding = embedder.embed_one(query)
    hits = store.search(query_embedding, top_k=top_k, min_score=min_score)

    if not hits:
        console.print(
            Panel(
                f"Nenhum resultado relevante para [bold]'{query}'[/].\n"
                f"(min_score={min_score})",
                title="Sem resultados",
                border_style="yellow",
            )
        )
        return

    table = Table(title=f"Resultados ({len(hits)} encontrados)", show_lines=True)
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Repositório", style="cyan", min_width=25)
    table.add_column("Score", justify="right", style="bold green", width=8)
    table.add_column("Trecho", max_width=80)

    for i, hit in enumerate(hits, 1):
        excerpt = hit["excerpt"][:200].replace("\n", " ")
        score_text = f"{hit['score']:.4f}"

        if hit["score"] >= 0.7:
            score_style = "bold green"
        elif hit["score"] >= 0.5:
            score_style = "bold yellow"
        else:
            score_style = "bold red"

        table.add_row(
            str(i),
            hit["repo_name"],
            Text(score_text, style=score_style),
            excerpt + "…",
        )

    console.print(table)
    console.print()


def cmd_stats(args: argparse.Namespace) -> None:
    init_db()
    store = get_vector_store()
    stats = store.stats()

    panel_content = (
        f"[bold]Tabela:[/]        {stats['table_name']}\n"
        f"[bold]Total chunks:[/]  {stats['total_chunks']}\n"
        f"[bold]Repositórios:[/]  {stats['unique_repos']}"
    )

    console.print()
    console.print(Panel(panel_content, title="Estatísticas da Base", border_style="cyan"))
    console.print()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="synapse-cli",
        description="Synapse — Buscador Semântico de Repositórios",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    idx = sub.add_parser("index", help="Indexar READMEs na base vetorial")
    idx.add_argument("--file", "-f", help="Caminho para um arquivo .md")
    idx.add_argument("--dir", "-d", help="Diretório com arquivos .md")
    idx.add_argument("--repo", "-r", help="Nome do repositório (usado com --file)")

    srch = sub.add_parser("search", help="Busca semântica na base de READMEs")
    srch.add_argument("query", help="Texto da busca")
    srch.add_argument("--top-k", type=int, default=10, help="Número máximo de resultados")
    srch.add_argument("--min-score", type=float, default=0.30, help="Score mínimo")

    sub.add_parser("stats", help="Estatísticas da base vetorial")

    return parser


def main() -> None:
    known_commands = {"index", "search", "stats", "-h", "--help"}
    if len(sys.argv) > 1 and sys.argv[1] not in known_commands:
        sys.argv.insert(1, "search")

    parser = build_parser()
    args = parser.parse_args()

    dispatch = {
        "index": cmd_index,
        "search": cmd_search,
        "stats": cmd_stats,
    }

    dispatch[args.command](args)


if __name__ == "__main__":
    main()
