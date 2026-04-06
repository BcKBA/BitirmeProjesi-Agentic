# Prompt Templates — Deep Agent Development

Use these templates when asking Antigravity or Copilot Chat to help with the Deep Agent backend.
File location in repo: `backend/agents/deep_agent/`

---

## Base Context Block (always prepend)

```
Project: AI Agent chatbot comparing Deep Agent vs Baseline Agent on SWE-QA dataset.
Repo: BcKBA/BitirmeProjesi-Agentic (monorepo), working in backend/agents/deep_agent/
Stack: Python 3.13, uv, deepagents>=0.4.12, langgraph, langchain-google-genai.
LLM: google_genai:gemini-2.5-flash (Paid tier 1). Fallback: gemini-2.0-flash-lite.
Deployment: langgraph dev → graph ID "agent" on localhost:2024.
Shared utils: backend/shared/repo_utils.py (clone_repo, build_file_tree, read_text_file).
Rules:
  - Use uv (not pip)
  - Check LangChain Docs MCP and DeepWiki MCP for current API syntax
  - Do not hardcode API keys — use .env + python-dotenv
  - Keep code minimal, no unnecessary abstractions
```

---

## Add a Custom Tool to the Agent

```
[Base Context Block]
Current tools.py: [paste backend/agents/deep_agent/tools.py]
Current agent.py: [paste backend/agents/deep_agent/agent.py]

Task: Add a custom tool to the Deep Agent that [describe what the tool does].
The tool should be decorated with @tool (from langchain_core.tools).
LangChain uses the docstring as the tool description — keep it clear.
If the tool needs repo cloning, import clone_repo from shared.repo_utils.
Add it to the tools=[] list in create_deep_agent() in agent.py.
Check deepagents documentation via DeepWiki MCP for the correct tool signature format.
```

---

## Debug an Error

```
[Base Context Block]
I got this error when running `uv run langgraph dev` (from backend/ directory):
[paste full error traceback]

Relevant files:
- backend/agents/deep_agent/agent.py: [paste content]
- backend/agents/deep_agent/tools.py: [paste content]
- backend/shared/repo_utils.py: [paste content if relevant]

Task: Identify the root cause and fix it. Check LangChain Docs MCP if it's a library API issue.
```

---

## Add a New LLM Provider

```
[Base Context Block]
Current model in agent.py: init_chat_model("google_genai:gemini-2.5-flash")

Task: Add support for [OpenRouter / Anthropic / Groq] as an alternative LLM provider.
Use an environment variable to switch (e.g., LLM_PROVIDER=google or openrouter).
Do not break the existing Google Gemini setup.
Check LangChain Docs MCP for init_chat_model() provider syntax and required packages.
```

---

## Test the Agent Directly

```
[Base Context Block]

Task: Write a simple test script (backend/test_deep_agent.py) that:
1. Imports the agent from agents/deep_agent/agent.py
2. Sends the message: "What repositories are available on this machine?"
3. Prints the agent's response
4. Does NOT require langgraph dev to be running
Run with: uv run python test_deep_agent.py (from backend/ directory)
Check deepagents documentation via DeepWiki MCP for how to invoke the agent directly.
```
