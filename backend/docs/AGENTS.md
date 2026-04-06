# AI Agent Usage Guide

This file defines which AI coding tool to use for which tasks in this project.
All tools use MCP servers: `langchain-docs` and `deepwiki` — always let them query these before writing any LangChain/deepagents code.

---

## Claude Code (this tool — VS Code extension)

**Best for:**
- File creation, editing, reading
- Running terminal commands (`uv add`, `git`, `langgraph dev`, `pnpm`)
- Planning and architecture decisions
- Debugging Python and TypeScript errors
- Git operations and project setup

**When to use:** Primary tool for backend Python work, file edits, and project setup.

**Important:** Claude Code does NOT have access to internet by default — use `WebSearch` tool when needed.

---

## Antigravity (Gemini Pro)

**Best for:**
- Long multi-file refactors (backend or frontend)
- Generating boilerplate code from descriptions
- Explaining complex LangChain/LangGraph/deepagents concepts (via DeepWiki MCP)
- Frontend (Next.js / TypeScript) changes with LangGraph SDK

**Prompt tips:**
- Always prepend: "Use the DeepWiki MCP and LangChain Docs MCP to check the latest documentation"
- Specify: "Use `uv` not `pip`" (backend) or "Use `pnpm` not `npm`" (frontend)
- Specify which agent you're touching: Deep Agent or Baseline Agent

---

## GitHub Copilot (VS Code inline)

**Best for:**
- Inline code completion while typing
- Quick docstrings and type hints
- Small, localized edits within a single file

**Prompt tips (Copilot Chat):**
- Use `#file:agent.py` or `#file:tools.py` to give context
- Say: "Use LangChain Docs MCP for up-to-date syntax"

---

## Token Optimization Strategy

| Situation | Action |
|-----------|--------|
| Simple edit (1-5 lines) | Copilot inline |
| Medium task (1 file) | Claude Code |
| Large refactor (multiple files) | Antigravity |
| Need latest LangChain/deepagents docs | Always invoke MCP in prompt |
| Gemini rate-limited | Switch to `gemini-2.0-flash-lite` in `.env` |
| Frontend (Next.js) change | Antigravity or Claude Code |

---

## Standard Prompt Prefix

### Backend (Deep Agent)

```
Project: AI Agent chatbot — Deep Agent vs Baseline Agent comparison on SWE-QA dataset.
Stack: Python 3.13, uv, deepagents>=0.4.12, langgraph, langchain-google-genai.
Repo: BcKBA/BitirmeProjesi-Agentic — monorepo, backend/ and frontend/ directories.
LLM: google_genai:gemini-2.5-flash (Paid tier 1). Fallback: gemini-2.0-flash-lite.
Rules:
  - Use uv (not pip)
  - Check LangChain Docs MCP and DeepWiki MCP before writing agent/tool code
  - Do not hardcode API keys — use .env + python-dotenv
  - Deep Agent only: create_deep_agent from deepagents
  - Shared utils in backend/shared/repo_utils.py — do not duplicate
File: [paste relevant file or describe what you need]
Task: [your actual request]
```

### Backend (Baseline Agent)

```
Project: AI Agent chatbot — Baseline (ReAct-style) Agent.
Stack: Python 3.13, uv, langchain, langchain-google-genai, faiss-cpu.
Repo: BcKBA/BitirmeProjesi-Agentic — backend/agents/baseline_agent/
LLM: google_genai:gemini-2.5-flash.
STRICT CONSTRAINT: This agent has exactly 3 tools: read_file, get_repo_structure, search_rag.
Do NOT add shell, planning, filesystem writing, or any other tools.
Rules:
  - Use uv (not pip)
  - Check LangChain Docs MCP for create_agent() syntax
  - Shared utils in backend/shared/repo_utils.py
File: [paste relevant file]
Task: [your actual request]
```

### Frontend (Next.js)

```
Project: AI Agent chatbot frontend — Deep Agents UI fork (Next.js).
Stack: Next.js, TypeScript, pnpm, @langchain/langgraph-sdk, Tailwind CSS.
Repo: BcKBA/BitirmeProjesi-Agentic — frontend/ directory.
Backend: langgraph dev on localhost:2024, graphs: "agent" (deep) and "baseline_agent".
Rules:
  - Use pnpm (not npm)
  - activeAgentId state controls which graph the useChat hook connects to
  - Check LangChain Docs MCP for @langchain/langgraph-sdk API
File: [paste relevant file]
Task: [your actual request]
```
