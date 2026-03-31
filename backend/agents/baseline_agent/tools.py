"""Tools for the Baseline (ReAct-style) Agent.

Strictly limited to the three tools defined in the SWE-QA paper:
  1. read_file
  2. get_repo_structure
  3. search_rag

No shell access, no planning, no filesystem writing, no extra utilities.
"""

import os
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from shared.repo_utils import build_file_tree, clone_repo, read_text_file

MAX_FILE_BYTES = 8_000

# In-memory RAG index cache keyed by repo path
_rag_indexes: dict[str, FAISS] = {}

# Separate embeddings for indexing vs. querying — different task_type yields better retrieval
_doc_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    task_type="RETRIEVAL_DOCUMENT",
)
_query_embeddings = GoogleGenerativeAIEmbeddings(
    model="models/text-embedding-004",
    task_type="RETRIEVAL_QUERY",
)


def _get_or_build_index(repo_path: str) -> FAISS:
    """Build (or return cached) a FAISS index for all text files in repo_path."""
    if repo_path in _rag_indexes:
        return _rag_indexes[repo_path]

    _, file_paths = build_file_tree(repo_path)
    docs: list[Document] = []
    for path in file_paths:
        content = read_text_file(path, MAX_FILE_BYTES)
        if content.strip():
            rel = str(Path(path).relative_to(repo_path))
            docs.append(Document(page_content=content, metadata={"source": rel, "abs_path": path}))

    index = FAISS.from_documents(docs, _doc_embeddings)
    _rag_indexes[repo_path] = index
    return index


def _resolve_repo(repo_url_or_path: str) -> tuple[str, None] | tuple[None, str]:
    """Return local path for a URL (clones if needed) or a local path as-is."""
    if repo_url_or_path.startswith("http://") or repo_url_or_path.startswith("https://"):
        return clone_repo(repo_url_or_path)
    if Path(repo_url_or_path).is_dir():
        return repo_url_or_path, None
    return None, f"Path not found: {repo_url_or_path}"


@tool
def read_file(file_path: str) -> str:
    """Read the contents of a specific file in the repository.
    Provide the absolute path to the file."""
    if not Path(file_path).is_file():
        return f"File not found: {file_path}"
    return read_text_file(file_path, MAX_FILE_BYTES)


@tool
def get_repo_structure(repo_url_or_path: str) -> str:
    """Get the directory tree of a repository.
    Accepts a GitHub URL (will be cloned) or a local filesystem path.
    Returns the file tree with absolute paths — use these paths with read_file."""
    local_path, error = _resolve_repo(repo_url_or_path)
    if error:
        return error
    tree, _ = build_file_tree(local_path)
    return f"Repository structure for: {repo_url_or_path}\n\n{tree}"


@tool
def search_rag(query: str, repo_url_or_path: str, top_k: int = 5) -> str:
    """Semantically search the repository codebase for content relevant to the query.
    Accepts a GitHub URL (will be cloned) or a local filesystem path.
    Returns the top_k most relevant file excerpts."""
    local_path, error = _resolve_repo(repo_url_or_path)
    if error:
        return error

    try:
        index = _get_or_build_index(local_path)
    except Exception as e:
        return f"Failed to build search index: {e}"

    results = index.similarity_search_by_vector(
        _query_embeddings.embed_query(query), k=top_k
    )
    if not results:
        return "No relevant results found."

    parts = []
    for i, doc in enumerate(results, 1):
        source = doc.metadata.get("source", "unknown")
        parts.append(f"[{i}] {source}\n{'-'*40}\n{doc.page_content}")
    return "\n\n".join(parts)
