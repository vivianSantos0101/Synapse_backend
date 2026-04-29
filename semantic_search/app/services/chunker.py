import re

def _clean_markdown(text: str) -> str:
    text = re.sub(r"```[\s\S]*?```", "", text)             
    text = re.sub(r"`[^`]+`", "", text)                    
    text = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text)  
    text = re.sub(r"!\[.*?\]\(.*?\)", "", text)            
    text = re.sub(r"\*{1,3}([^*]+)\*{1,3}", r"\1", text)  
    text = re.sub(r"<[^>]+>", "", text)                    
    text = re.sub(r"^-{3,}$", "", text, flags=re.MULTILINE)  
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip().lower()

def _project_name(repo_name: str) -> str:
    return repo_name.split("/")[-1].lower()

def _is_empty_after_clean(text: str) -> bool:
    words = re.findall(r"\b\w{3,}\b", text)
    return len(words) < 5  

def chunk_readme(content: str, repo_name: str, min_chunk_size: int = 50) -> list[dict]:
    project = _project_name(repo_name)
    parts = re.split(r'\n\s*\n', content)
    chunks = []

    for part in parts:
        part = part.strip()
        if not part:
            continue

        clean = _clean_markdown(part)

        if len(clean) < min_chunk_size or _is_empty_after_clean(clean):
            continue

        enriched = f"{project}: {clean}"

        chunks.append({
            "text": enriched,
            "repo_name": repo_name,
        })

    if not chunks:
        clean = _clean_markdown(content)
        if clean and not _is_empty_after_clean(clean):
            chunks.append({
                "text": f"{project}: {clean}",
                "repo_name": repo_name,
            })

    return chunks