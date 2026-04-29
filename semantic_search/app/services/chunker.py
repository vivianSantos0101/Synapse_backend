"""Divide README.md em chunks por seção (headings)."""
import re


def _clean_markdown(text: str) -> str:
    text = re.sub(r"```[\s\S]*?```", "", text)             # remove blocos de código
    text = re.sub(r"`[^`]+`", "", text)                    # remove inline code
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)  # links → texto
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)            # remove imagens
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)  # bold/italic
    text = re.sub(r"<[^>]+>", "", text)                    # tags HTML
    text = re.sub(r"^-{3,}$", "", text, flags=re.MULTILINE)  # remove linhas ---
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip().lower()


def _project_name(repo_name: str) -> str:
    """Extrai só o nome do projeto. Ex: 'empresa/nebula' → 'nebula'"""
    return repo_name.split("/")[-1].lower()


def _is_empty_after_clean(text: str) -> bool:
    """Retorna True se o texto não tem conteúdo semântico real após limpeza.
    
    Seções que eram quase 100% código (ex: Entry com só JSON, Execução com
    só comandos bash) viram lixo após remover os blocos — ficam com frases
    curtas sem sentido como 'cada item armazenado no cache:' ou
    'modo standalone: modo cluster:'. Esses chunks poluem o banco.
    """
    # Remove pontuação e espaços para contar palavras reais
    words = re.findall(r"\b\w{3,}\b", text)
    return len(words) < 5  # menos de 5 palavras com 3+ letras = sem conteúdo


def chunk_readme(content: str, repo_name: str, min_chunk_size: int = 30) -> list[dict]:
    sections = re.split(r"(?m)^(#{1,3} .+)$", content)
    chunks = []
    current_heading = "Introdução"
    project = _project_name(repo_name)

    for part in sections:
        part = part.strip()
        if not part:
            continue

        if re.match(r"^#{1,3} ", part):
            current_heading = re.sub(r"^#+\s*", "", part).strip()
            continue

        clean = _clean_markdown(part)

        # Descarta chunks sem conteúdo semântico real (seções só de código)
        if len(clean) < min_chunk_size or _is_empty_after_clean(clean):
            continue

        # Enriquece com projeto + seção como prefixo natural.
        # "nebula - roadmap: dashboard web..." ancora o vetor semanticamente
        # ao projeto e ao contexto, aumentando scores para buscas diretas.
        enriched = f"{project} - {current_heading.lower()}: {clean}"

        chunks.append({
            "text": enriched,
            "section": current_heading,
            "repo_name": repo_name,
        })

    # Fallback: README inteiro se não gerou chunks
    if not chunks:
        clean = _clean_markdown(content)
        if clean:
            chunks.append({
                "text": f"{project} - readme completo: {clean}",
                "section": "README completo",
                "repo_name": repo_name,
            })

    return chunks