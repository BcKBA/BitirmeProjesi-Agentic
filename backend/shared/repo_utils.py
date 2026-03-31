"""Shared repository utilities used by both deep_agent and baseline_agent."""

import tempfile
from pathlib import Path

import git

TEXT_EXTENSIONS = {
    ".py", ".js", ".ts", ".jsx", ".tsx", ".md", ".txt", ".json",
    ".yaml", ".yml", ".toml", ".cfg", ".ini", ".sh", ".env.example",
    ".html", ".css", ".rs", ".go", ".java", ".cpp", ".c", ".h",
}
SKIP_DIRS = {".git", "__pycache__", "node_modules", ".venv", "venv", "dist", "build"}

# Cache cloned repos so we don't re-clone on follow-up questions
_cloned_repos: dict[str, str] = {}


def clone_repo(repo_url: str) -> tuple[str, None] | tuple[None, str]:
    """Clone a public GitHub repo (cached). Returns (local_path, None) or (None, error_message)."""
    if repo_url in _cloned_repos:
        return _cloned_repos[repo_url], None
    tmp = tempfile.mkdtemp()
    try:
        git.Repo.clone_from(repo_url, tmp, depth=1)
    except Exception as e:
        return None, f"Failed to clone {repo_url}: {e}"
    _cloned_repos[repo_url] = tmp
    return tmp, None


def build_file_tree(
    root_path: str,
    max_lines: int = 400,
    max_files: int = 200,
) -> tuple[str, list[str]]:
    """Return (tree_string, list_of_text_file_paths) for a directory."""
    root = Path(root_path)
    tree_lines: list[str] = []
    file_paths: list[str] = []

    for dirpath, dirs, files in root.walk() if hasattr(root, "walk") else _os_walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        try:
            level = len(Path(dirpath).relative_to(root).parts)
        except ValueError:
            level = 0
        folder = Path(dirpath).name or root.name
        tree_lines.append("  " * level + folder + "/")
        for f in files:
            full = Path(dirpath) / f
            tree_lines.append("  " * (level + 1) + f + f"  [path: {full}]")
            if full.suffix.lower() in TEXT_EXTENSIONS and len(file_paths) < max_files:
                file_paths.append(str(full))

    return "\n".join(tree_lines[:max_lines]), file_paths


def _os_walk(root: Path):
    """Fallback for Python < 3.12 that doesn't have Path.walk()."""
    import os
    for dirpath, dirs, files in os.walk(root):
        yield dirpath, dirs, files


def read_text_file(path: str, max_bytes: int = 4_000) -> str:
    """Read a text file safely, returning its content up to max_bytes."""
    try:
        return Path(path).read_text(encoding="utf-8", errors="ignore")[:max_bytes]
    except Exception as e:
        return f"Error reading {path}: {e}"
