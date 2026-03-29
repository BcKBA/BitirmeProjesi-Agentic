# Deep Agent Backend

A software repository analysis agent built with [LangChain Deep Agents](https://github.com/langchain-ai/deep-agents) and Google Gemini. The agent can analyze both GitHub repositories and local codebases, answering questions about architecture, code structure, and logic.

## Features

- Clone and analyze public GitHub repositories
- Analyze local repositories
- Read specific files on demand
- Built-in Deep Agent tools: Planning, Virtual Filesystem, Shell, Sub-agents, Context Summarization
- Interactive UI via LangGraph Studio

## Tech Stack

- **Language:** Python 3.13+
- **Agent Framework:** [deepagents](https://pypi.org/project/deepagents/)
- **LLM:** Google Gemini (`gemini-2.5-flash-lite`)
- **Serving:** LangGraph CLI (`langgraph dev`)
- **Package Manager:** [uv](https://github.com/astral-sh/uv)

## Getting Started

### 1. Install dependencies

```bash
uv sync
```

### 2. Set up environment variables

Create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key
LANGCHAIN_API_KEY=your_langchain_api_key
LANGCHAIN_TRACING_V2=true
```

### 3. Run the agent

```bash
uv run langgraph dev
```

This starts the server at `http://127.0.0.1:2024` and opens LangGraph Studio in your browser.

## Usage

Send a message to the agent with a GitHub URL or a local path:

```
Analyze the repository at https://github.com/fastapi/fastapi and describe its architecture.
```

```
Analyze the local repository at /path/to/your/project and describe its architecture.
```

## Project Structure

```
.
├── agent.py          # Deep Agent definition and custom tools
├── main.py           # Entry point
├── pyproject.toml    # Project dependencies (uv)
├── langgraph.json    # LangGraph configuration
└── .env              # API keys (not committed)
```
