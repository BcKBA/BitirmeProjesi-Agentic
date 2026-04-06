# Claude Code Instructions

## Startup Rule

**Her chat başında:** `backend/docs/CONTEXT.md` dosyasını oku. Tüm mimari kararlar, repo yapısı ve teknoloji stack'i orada.

## Project Context

AI Agent chatbot comparing two architectures on the SWE-QA dataset:

- **Deep Agent**: `create_deep_agent` from `deepagents` — hierarchical, sub-agents, planning, VFS
- **Baseline Agent**: `create_agent` from `langchain.agents` — ReAct-style, exactly 3 tools

Goal: Academic paper comparing performance and efficiency of both architectures.

Active repo: **BcKBA/BitirmeProjesi-Agentic** (monorepo — `backend/` + `frontend/`)
Full context: `backend/docs/CONTEXT.md`

## Core Rules

- **No manual coding** — all code via prompting (Claude Code, Antigravity, Copilot)
- **uv only** for Python deps — never `pip`
- **pnpm only** for frontend deps — never `npm install`
- **`.env` never committed** — secrets in `.env`, examples in `.env.example`
- **PROGRESS.md güncelle** — her tamamlanan adımdan sonra (`backend/docs/PROGRESS.md`)

## Package Manager

```bash
# Backend (backend/ dizininden çalıştır)
uv add <package>
uv run langgraph dev

# Frontend (frontend/ dizininden çalıştır)
pnpm install
pnpm dev
```

## MCP Servers (her LangChain/deepagents kodu yazılmadan önce sorgula)

| Server | Transport |
|---|---|
| DeepWiki MCP | `https://mcp.deepwiki.com/mcp` |
| LangChain MCP | `npx -y langchain-mcp` |
| GitHub MCP | `npx -y @modelcontextprotocol/server-github` |

**Kural:** LangChain, LangGraph, deepagents veya `@langchain/langgraph-sdk` kodu yazmadan önce mutlaka ilgili MCP'yi sorgula. Bu kütüphaneler sık değişir.

## Agent Architecture — Quick Reference

**Deep Agent** (`backend/agents/deep_agent/`)
- `agent.py`: `create_deep_agent(model, tools=[...], system_prompt=...)`
- `tools.py`: `find_local_repos`, `clone_and_read_repo`, `read_local_repo`, `read_repo_file`
- LangGraph graph ID: `"agent"`

**Baseline Agent** (`backend/agents/baseline_agent/`)
- `agent.py`: `create_agent(model, tools=[read_file, get_repo_structure, search_rag], ...)`
- `tools.py`: `read_file`, `get_repo_structure`, `search_rag` (FAISS RAG) — **başka araç ekleme**
- LangGraph graph ID: `"baseline_agent"`

**Shared** (`backend/shared/repo_utils.py`)
- `clone_repo()`, `build_file_tree()`, `read_text_file()` — her iki agent kullanır

**Frontend** (`frontend/`)
- `src/components/thread/agent-selector.tsx`: Standard / Deep Agent dropdown
- `activeAgentId` → `useChat` hook → `langgraph-sdk`

## File Editing Rules

- Remove HTML comments when editing any file.
- Keep `.env` files out of git.
- Do not add docstrings or comments to code you didn't change.
- Minimal changes — istenenden fazlasını yapma.
