# Security Guidelines

## API Key Management

### Rules
1. **Never commit `.env`** — it is in `.gitignore`. Verify before every push: `git status` must not show `.env`.
2. **Never hardcode API keys** in Python or TypeScript files. Always use `os.getenv()` / `python-dotenv` (backend) or `.env.local` / `process.env` (frontend).
3. **Never share keys in chat** (not with Claude, Copilot, or Antigravity).
4. **Frontend `.env.local` da commit edilmez** — `frontend/.gitignore` bunu kapsar.

### Current Keys Required

| Key | Where to Get | Where to Set |
|-----|-------------|--------------|
| `GOOGLE_API_KEY` | https://aistudio.google.com/app/apikey | `backend/.env` |
| `LANGSMITH_API_KEY` (optional, tracing) | https://smith.langchain.com | `backend/.env` |
| `OPENAI_API_KEY` (optional, OpenRouter fallback) | https://openrouter.ai/keys | `backend/.env` |

### `backend/.env` Template

```env
GOOGLE_API_KEY=your_key_here

# Optional — LangSmith tracing
# LANGSMITH_API_KEY=your_langsmith_key
# LANGSMITH_TRACING=true

# Optional — OpenRouter fallback
# OPENAI_API_KEY=your_openrouter_key
# OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

### `frontend/.env.local` Template

```env
# LangGraph backend URL (for production deployment)
# NEXT_PUBLIC_API_URL=http://localhost:2024
```

## If a Key is Accidentally Committed

1. Immediately revoke the key in the provider dashboard
2. Generate a new key
3. Run BFG Repo Cleaner or `git filter-branch` to purge key from history
4. Force push (coordinate with Berat Can)

## Shell Tool Safety

The Deep Agent has a `Shell` tool that can run arbitrary commands.
- Development (`langgraph dev`): shell runs with your user permissions — be careful what you ask the agent to do
- Never run `langgraph dev` as admin/root
- Do not give the agent instructions to delete files or run destructive commands
