# GitHub Copilot Workspace Instructions

## Project Context

This project aims to develop an AI Agent chatbot that answers complex questions about software repository architecture and logic. Two different agent architectures are compared:

- **ReAct Agent**: A multi-step agent based on the "Reason-then-Act" loop
- **Deep Agent**: An agent using hierarchical architecture, task decomposition, and sub-agents

Goal: Produce an academic paper comparing the performance and efficiency of these two architectures on the **SWE-QA dataset**.

## Core Rule: No Manual Coding

**Writing code manually is not allowed in this project.** All code generation must be done by prompting Code Agents (Copilot, Claude Code, etc.). Copilot's role is to understand the user's request, generate the correct code, and fix errors by consulting LangChain/DeepWiki documentation.

## Package Manager Rule

- Always use **`uv`** for Python dependencies, never `pip`.
- Example: `uv add langchain`, `uv run python main.py`

## MCP Servers

- DeepWiki MCP: `https://mcp.deepwiki.com/mcp`
- LangChain MCP: `npx -y langchain-mcp`
- GitHub MCP: `npx -y @modelcontextprotocol/server-github` (requires token)

## MCP Usage and Prompt Guidelines

1. Always specify when generating code:
   - "Use DeepWiki MCP and LangChain MCP for up-to-date documentation lookup."
   - "Do not use stale local docs."
2. Ensure endpoint connections are active:
   - `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable must be set.
   - `langchain-mcp` and `@modelcontextprotocol/server-github` processes must be running.
3. Prompt example:
   - `In your code suggestion, query DeepWiki MCP and LangChain MCP first for the latest LangChain/Deep Agents docs.`

## Agent Architecture-Specific Instructions

- **ReAct Agent** implementations: Use LangChain's `create_react_agent` API and verify the latest syntax via DeepWiki MCP.
- **Deep Agent** implementations: Refer to LangChain Deep Agents documentation; apply hierarchical planning, task decomposition, and sub-agent patterns. Use this architecture to solve context overflow issues.
- For both agents, handle tool calling, prompt templating, and memory management according to up-to-date docs via LangChain MCP.

## File Editing Rules

- Remove HTML comments from files.
- The MCP server condition must be repeated in every new Copilot request.

## Copilot Instruction (Workspace Rule Set)

The following instructions are the permanent rule set governing Copilot behavior for this repository:

- _Copilot must include the following in every code suggestion:_
  - "Use DeepWiki MCP and LangChain MCP for up-to-date documentation lookup."
  - "Do not use stale local docs."
- _MCP endpoint connections must be verified:_
  - `GITHUB_PERSONAL_ACCESS_TOKEN` environment variable must be set.
  - `langchain-mcp` and `@modelcontextprotocol/server-github` processes must be running.
- _In all suggestions, authoritative MCP sources (DeepWiki/LangChain Docs) must be queried first._
- _Always use `uv` for Python package installations, never `pip`._
- _Code must be written on behalf of the user; the user must not write code themselves._
- _This file is presented to Copilot as an 'instruction' defined in `copilot-instructions.md`._
