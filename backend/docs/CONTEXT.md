# CONTEXT.md — Project Master Reference

> **Yeni chat veya model başlatırken tek komut:**
> `"Read CONTEXT.md at c:\bitirme and follow all rules and links inside it before doing anything."`
>
> Bu dosyayı okuyan her model şunları bilir: proje bağlamı, kurallar, mevcut ilerleme, araç seçimleri.
> Detay için: PROGRESS.md (neredeyiz) · DECISIONS.md (neden) · AGENTS.md (hangi AI aracı ne zaman) · SECURITY.md (key yönetimi)

---

## Mandatory Rules (her model her zaman uymak zorunda)

1. **Package manager: `uv`** — `pip` ASLA kullanma. Paket eklemek için: `uv add <pkg>`. Çalıştırmak için: `uv run <cmd>`.
2. **API keys: `.env` dosyasında** — kod içine hardcode etme. `python-dotenv` ile yükle.
3. **Her değişiklikten sonra push** — `gh` CLI ile commit + push yap (bkz. Git Workflow bölümü).
4. **Her değişiklikten sonra PROGRESS.md güncelle** — tamamlanan adımı işaretle, yeni adım varsa ekle.
5. **MCP kullan** — LangChain veya deepagents kodu yazarken mutlaka `langchain-docs` ve `deepwiki` MCP'yi sorgula. Eski dokümantasyonla yanlış kod yazma.
6. **Minimal değişiklik** — istenenden fazlasını yapma, gereksiz abstraction ekleme, docstring/yorum ekleme.
7. **Bu repo Berat Can Karakaş'ın reposunun kopyasıdır** — orijinal: `BcKBA/BitirmeProjesi-Agentic`. Değişiklikler orada yapılır, burası takip amaçlıdır.

---

## What This Project Is

An AI Agent chatbot that answers complex questions about software repository architecture and logic.
Two agent architectures are implemented and compared:

- **Deep Agent** (`deepagents.create_deep_agent`) — hierarchical, uses sub-agents, planning, virtual filesystem, context summarization
- **Baseline Agent** (`langchain.agents.create_agent`, ReAct-style) — 3 tool constraint: `read_file`, `get_repo_structure`, `search_rag`

Final deliverable: a research paper comparing both architectures on the **SWE-QA dataset**.

---

## Scope & Status

| Component | Description | Status |
|-----------|-------------|--------|
| Deep Agent backend | `agents/deep_agent/agent.py` — deepagents + custom tools | Week 2 — Complete |
| Baseline Agent backend | `agents/baseline_agent/agent.py` — create_agent + 3 tools | Week 3 — Complete |
| Shared utilities | `shared/repo_utils.py` — clone, file tree, text reader | Complete |
| Frontend UI | Next.js, agent dropdown selector (Standard / Deep Agent) | Week 3 — Complete |
| SWE-QA Evaluation | Benchmark both agents on dataset | Later |
| Research Paper | Academic comparison of both architectures | Final |

---

## Architecture

```
User (browser)
    ↓
Next.js Frontend (frontend/)
    — agent-selector dropdown (standard_agent / deep_agent)
    — useChat hook with activeAgentId
    — @langchain/langgraph-sdk
    ↓
langgraph dev server  (localhost:2024)
    ↓
langgraph.json  →  graphs:
    "agent"          → agents/deep_agent/agent.py:agent
    "baseline_agent" → agents/baseline_agent/agent.py:agent
    ↓
Deep Agent path:
    create_deep_agent(model, tools=[find_local_repos, clone_and_read_repo, read_local_repo, read_repo_file])
    Default tools: Planning, VirtualFilesystem, Shell, Sub-agents, ContextSummarization
    LLM: google_genai:gemini-2.5-flash

Baseline Agent path:
    create_agent(model, tools=[read_file, get_repo_structure, search_rag])
    RAG: FAISS in-memory, GoogleGenerativeAIEmbeddings (text-embedding-004)
    LLM: google_genai:gemini-2.5-flash
```

---

## Repository Structure (Berat Can'ın Reposu: BcKBA/BitirmeProjesi-Agentic)

```
BitirmeProjesi-Agentic/
  backend/
    agents/
      deep_agent/
        agent.py          ← create_deep_agent tanımı
        tools.py          ← find_local_repos, clone_and_read_repo, read_local_repo, read_repo_file
        PROMPT.md         ← Deep Agent için vibe-coding prompt şablonları
      baseline_agent/
        agent.py          ← create_agent tanımı (3 araç)
        tools.py          ← read_file, get_repo_structure, search_rag (FAISS RAG)
        PROMPT.md         ← Baseline Agent için vibe-coding prompt şablonları
    shared/
      repo_utils.py       ← clone_repo, build_file_tree, read_text_file (her iki agent paylaşır)
    docs/
      CONTEXT.md / PROGRESS.md / DECISIONS.md / AGENTS.md / SECURITY.md
    langgraph.json        ← "agent" ve "baseline_agent" graph tanımları
    pyproject.toml        ← uv bağımlılıkları
    main.py
    .env                  ← API keys (commit edilmez)

  frontend/
    src/
      components/thread/
        agent-selector.tsx  ← Standard / Deep Agent dropdown
        index.tsx
      providers/
        Stream.tsx
        Thread.tsx
        client.ts
    package.json          ← pnpm ile yönetilir
    next.config.mjs
```

---

## Tech Stack

| Layer | Choice | Reason |
|-------|--------|--------|
| Language | Python 3.13 | LangChain ekosistemi |
| Package manager (backend) | uv | Hızlı, lockfile, proje şartı |
| Package manager (frontend) | pnpm | Next.js projesinin varsayılanı |
| Agent framework | deepagents ≥ 0.4.12 | Deep Agent için proje şartı |
| Baseline agent | langchain `create_agent()` | ReAct-style, SWE-QA kısıtlaması |
| Vector store | FAISS (in-memory) | search_rag için, hosted DB gerekmez |
| Embeddings | GoogleGenerativeAIEmbeddings text-embedding-004 | Ücretsiz, Gemini ile uyumlu |
| LLM provider | google_genai:gemini-2.5-flash | AI Studio paid tier 1 (10K RPD) |
| Deployment | langgraph dev | Her iki graph aynı port'tan (2024) |
| Frontend | Next.js + @langchain/langgraph-sdk | Deep Agents UI fork |

---

## Key Files — Hızlı Referans

| Dosya | Ne yapar |
|-------|----------|
| `backend/agents/deep_agent/agent.py` | Deep Agent tanımı, model, system prompt, tool listesi |
| `backend/agents/deep_agent/tools.py` | find_local_repos, clone_and_read_repo, read_local_repo, read_repo_file |
| `backend/agents/baseline_agent/agent.py` | Baseline Agent, model, system prompt, 3 araç |
| `backend/agents/baseline_agent/tools.py` | read_file, get_repo_structure, search_rag (FAISS) |
| `backend/shared/repo_utils.py` | clone_repo(), build_file_tree(), read_text_file() — paylaşılan utils |
| `backend/langgraph.json` | "agent" → deep, "baseline_agent" → baseline, env: .env |
| `frontend/src/components/thread/agent-selector.tsx` | Kullanıcıya agent seçtiren dropdown |
| `frontend/src/providers/Stream.tsx` | activeAgentId → langgraph-sdk bağlantısı |

---

## Git Workflow

```bash
# backend değişikliği için (BcKBA repo'sunda)
cd <repo-dizini>/backend
git add <değişen dosyalar>
git commit -m "kısa açıklama"
git push

# frontend değişikliği için
cd <repo-dizini>/frontend
git add <değişen dosyalar>
git commit -m "kısa açıklama"
git push
```

**Araçlar:** `gh` CLI (v2.68.1) — `gh auth login` tamamlandı (alperenkayim). `uv` ve `gh` PATH'e kalıcı eklendi.

---

## Key Links

- LangGraph Studio: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
- Proje Reposu: https://github.com/BcKBA/BitirmeProjesi-Agentic
- Google AI Studio (API key): https://aistudio.google.com/app/apikey
- Instructor GitHub: https://github.com/amirkiarafiei
