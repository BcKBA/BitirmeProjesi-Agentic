# Prompt Templates — Baseline Agent Development

Use these templates when asking Claude Code or Copilot to help with the Baseline Agent.

---

## Base Context Block (always prepend)

```
Project: AI Agent chatbot comparing Baseline vs Deep Agent on SWE-QA dataset.
Stack: Python 3.13, uv package manager, langchain, langchain-google-genai.
LLM: Google Gemini 2.5 Flash via langchain-google-genai.
Agent type: Baseline (ReAct-style) — created with create_agent().
STRICT CONSTRAINT: This agent has exactly 3 tools: read_file, get_repo_structure, search_rag.
Do NOT add shell, planning, filesystem writing, or any other tools.
Rules:
  - Use uv (not pip)
  - Check LangChain Docs MCP and DeepWiki MCP for current API syntax
  - Do not hardcode API keys — use .env + python-dotenv
```

---

## Modify a Tool

```
[Base Context Block]
Current tools file: agents/baseline_agent/tools.py — [paste content]

Task: Modify the [read_file / get_repo_structure / search_rag] tool to [describe change].
Do NOT add new tools. Only modify the existing implementation.
Check LangChain Docs MCP for the correct tool/decorator syntax.
```

---

## Debug an Error

```
[Base Context Block]
I got this error when running `uv run langgraph dev`:
[paste full error traceback]

Relevant files:
- agents/baseline_agent/agent.py: [paste content]
- agents/baseline_agent/tools.py: [paste content]

Task: Identify the root cause and fix it.
```

---

## Improve RAG Quality

```
[Base Context Block]
Current search_rag implementation: [paste tools.py content]

Task: Improve the search_rag tool to better retrieve relevant code snippets.
Consider: chunking strategy, embedding model choice, top_k tuning.
Use langchain-google-genai embeddings (GoogleGenerativeAIEmbeddings).
Do NOT replace FAISS with a hosted vector store.
Check LangChain Docs MCP for the latest FAISS + LangChain integration.
```
