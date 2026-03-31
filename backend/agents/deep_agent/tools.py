"""Custom tools for the Deep Agent."""

import os
from pathlib import Path

from langchain_core.tools import tool

from shared.repo_utils import (
    SKIP_DIRS,
    TEXT_EXTENSIONS,
    build_file_tree,
    clone_repo,
    read_text_file,
)

MAX_FILE_BYTES = 4_000
MAX_TOTAL_CHARS = 40_000


@tool
def find_local_repos(search_dirs: list[str] | None = None) -> str:
    """Scan the local filesystem for git repositories and return their paths.
    Use this when the user asks which repositories exist on their computer.
    Searches common locations by default: ~/Projects, ~/Documents, ~/Desktop, ~/code, ~/dev, ~/src."""
    if search_dirs is None:
        home = os.path.expanduser("~")
        search_dirs = [
            os.path.join(home, d)
            for d in ("Projects", "Documents", "Desktop", "code", "dev", "src", "workspace")
        ]

    found = []
    for base in search_dirs:
        if not os.path.isdir(base):
            continue
        for root, dirs, _ in os.walk(base):
            if ".git" in dirs:
                found.append(root)
                dirs.clear()
                continue
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

    if not found:
        return f"No git repositories found in: {', '.join(search_dirs)}"

    lines = [f"Found {len(found)} git repositories:"]
    for path in sorted(found):
        lines.append(f"  {path}")
    return "\n".join(lines)


@tool
def clone_and_read_repo(repo_url: str) -> str:
    """Clone a public GitHub repository and return its file tree plus contents of key source files.
    Use this whenever the user provides a GitHub URL and wants to understand the codebase."""
    local_path, error = clone_repo(repo_url)
    if error:
        return error

    tree, file_paths = build_file_tree(local_path)

    file_contents = []
    total_chars = 0
    for path in file_paths:
        if total_chars >= MAX_TOTAL_CHARS:
            break
        content = read_text_file(path, MAX_FILE_BYTES)
        rel = str(Path(path).relative_to(local_path))
        snippet = f"\n{'='*60}\n# {rel}\n{'='*60}\n{content}"
        file_contents.append(snippet)
        total_chars += len(snippet)

    return (
        f"Repository cloned: {repo_url}\n\n"
        f"FILE TREE:\n{tree}\n\n"
        f"FILE CONTENTS (key files):\n{''.join(file_contents)}"
    )


@tool
def read_local_repo(repo_path: str) -> str:
    """Read a local repository directory and return its file tree plus contents of key source files.
    Use this when the user provides a local filesystem path (e.g. /Users/foo/myproject)."""
    if not Path(repo_path).is_dir():
        return f"Directory not found: {repo_path}"

    tree, file_paths = build_file_tree(repo_path)

    file_contents = []
    total_chars = 0
    for path in file_paths:
        if total_chars >= MAX_TOTAL_CHARS:
            break
        content = read_text_file(path, MAX_FILE_BYTES)
        rel = path.replace(repo_path, "").lstrip(os.sep)
        snippet = f"\n{'='*60}\n# {rel}\n{'='*60}\n{content}"
        file_contents.append(snippet)
        total_chars += len(snippet)

    return (
        f"Local repository: {repo_path}\n\n"
        f"FILE TREE:\n{tree}\n\n"
        f"FILE CONTENTS (key files):\n{''.join(file_contents)}"
    )


@tool
def read_repo_file(file_path: str) -> str:
    """Read a specific file from a previously cloned or local repository.
    Use the absolute path returned by clone_and_read_repo or read_local_repo."""
    return read_text_file(file_path, MAX_FILE_BYTES * 2)
