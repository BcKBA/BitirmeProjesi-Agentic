# Architecture Decisions

## ADR-001: Use `uv` instead of `pip`

**Decision:** Use `uv` as the package manager.
**Reason:** Project requirement. `uv` is significantly faster than `pip`, handles virtual environments automatically, and produces a lockfile (`uv.lock`) for reproducibility.
**How to apply:** Always use `uv add <package>` instead of `pip install`. Never run `pip` directly.

---

## ADR-002: Google Gemini (AI Studio) as LLM provider

**Decision:** Use `google_genai:gemini-2.5-flash` via Google AI Studio (Paid tier 1 account).
**Reason:** Free tier (20 RPD) was insufficient for development. Paid tier 1 provides 10K RPD for gemini-2.5-flash and unlimited RPD for gemini-2.0-flash-lite. Easy to set up with just `GOOGLE_API_KEY`. Switching to OpenRouter or other providers requires only changing one line in `agent.py`.
**How to apply:** Get API key from https://aistudio.google.com/app/apikey and put in `.env`.
**Fallback if rate-limited:** Switch to `gemini-2.0-flash-lite` (unlimited RPD on paid tier).
**Alternative:** OpenRouter — set `OPENAI_API_KEY` + `OPENAI_BASE_URL=https://openrouter.ai/api/v1` and change model string.

---

## ADR-003: Deep Agent before Baseline Agent

**Decision:** Implement Deep Agent first (Week 2), Baseline Agent later (Week 3).
**Reason:** Project assignment order. Deep Agent is more complex (hierarchical, sub-agents) so scaffolding it first establishes the shared infrastructure (`repo_utils.py`) for both.

---

## ADR-004: Custom frontend (Next.js) instead of LangGraph Studio

**Decision:** Week 3'te LangGraph Studio hosted UI yerine fork edilmiş Deep Agents UI (Next.js) kullanıldı.
**Reason:** Week 3 görevi agent seçici dropdown içeren özel UI gerektiriyor. `@langchain/langgraph-sdk` ile her iki agent'a tek frontend'den bağlanmak mümkün.
**How it works:** Frontend `activeAgentId` state'ini tutar. `useChat` hook bu ID'yi LangGraph client'a geçirir. Kullanıcı dropdown'dan seçince ilgili graph ID'ye (`agent` veya `baseline_agent`) bağlanır.

---

## ADR-005: Keep `.env` out of git

**Decision:** Never commit `.env` to the repository.
**Reason:** API keys would be exposed publicly. `.gitignore` excludes `.env`. Share keys only via secure channels.

---

## ADR-006: Monorepo — backend + frontend aynı repoda

**Decision:** `BcKBA/BitirmeProjesi-Agentic` tek repo, `backend/` ve `frontend/` alt dizinleri var.
**Reason:** Instructor'ın Week 3'te beklediği yapı bu. Hem frontend hem backend kodları aynı repoda yönetimi kolaylaştırır.
**Not:** Önceden ayrı repolar (`alperenkayim/bitirme-backend`, `alperenkayim/bitirme-frontend`) vardı, Week 3'te Berat Can'ın reposuna geçildi.

---

## ADR-007: Custom clone_and_read_repo tool instead of shell git

**Decision:** Add a custom `clone_and_read_repo` tool using `gitpython` library instead of relying on the agent's built-in shell tool to run `git clone`.
**Reason:** The Deep Agent's shell tool runs in a sandboxed environment with no access to the host system's `git` binary (`git --version` returned "No data"). Custom tool uses `gitpython` in-process, returns file tree + file contents directly to the agent — no VFS access needed.
**How to apply:** Tool is defined in `agents/deep_agent/tools.py`. Shared clone logic is in `shared/repo_utils.py`.

---

## ADR-008: Shared repo_utils.py for both agents

**Decision:** `backend/shared/repo_utils.py` içinde `clone_repo()`, `build_file_tree()`, `read_text_file()` fonksiyonları her iki agent tarafından import edilir.
**Reason:** Deep Agent ve Baseline Agent'ın repo okuma mantığı aynı. Tekrar eden kodu önlemek ve consistency sağlamak için paylaşılan utils çıkarıldı.
**How to apply:** `from shared.repo_utils import clone_repo, build_file_tree, read_text_file`

---

## ADR-009: FAISS in-memory RAG for Baseline Agent

**Decision:** Baseline Agent'ın `search_rag` tool'u için FAISS in-memory vektör store kullanıldı.
**Reason:** Hosted vector DB (Pinecone, Weaviate vb.) kurulumu gerektirmez. `faiss-cpu` ile sıfırdan index build edilir, repo path'e göre cache'lenir. SWE-QA paper'ın tanımladığı `search_rag` aracının minimal implementasyonu.
**How to apply:** `langchain_community.vectorstores.FAISS` + `GoogleGenerativeAIEmbeddings`. Index ilk `search_rag` çağrısında build edilir, sonrakiler cache'den döner.

---

## ADR-010: Baseline Agent strictly 3 tools only

**Decision:** Baseline Agent'a sadece `read_file`, `get_repo_structure`, `search_rag` verildi. Shell, planning, VFS veya başka araç yok.
**Reason:** SWE-QA paper'ın tanımladığı baseline agent kısıtlaması. Karşılaştırma geçerli olsun diye Deep Agent'ın ekstra kabiliyetleri Baseline'a taşınmaz.
