# Progress Log

## Week 3 — Agent Implementation & UI Integration (2026-04-05)

### Completed (Berat Can Karakaş ile birlikte — BcKBA/BitirmeProjesi-Agentic)
- [x] Baseline Agent (`create_agent`) implement edildi — `backend/agents/baseline_agent/agent.py`
- [x] Baseline Agent araçları implement edildi — `read_file`, `get_repo_structure`, `search_rag`
- [x] `search_rag` için FAISS in-memory RAG + `GoogleGenerativeAIEmbeddings` (text-embedding-004)
- [x] `backend/shared/repo_utils.py` oluşturuldu — her iki agent ortak utils'i paylaşıyor
- [x] `langgraph.json` güncellendi — `"agent"` (deep) + `"baseline_agent"` aynı port:2024'te
- [x] Frontend: Next.js agent-selector dropdown — Standard Agent / Deep Agent
- [x] Frontend: `activeAgentId` state → `useChat` hook → `langgraph-sdk` dinamik bağlantı
- [x] Uçtan uca test tamamlandı — her iki agent UI'dan çalışıyor
- [x] Repo monorepo yapısına taşındı: `backend/` + `frontend/` tek repo içinde

### In Progress
- [ ] Instructor collaborator invite kabulü (amirkiarafiei tarafında bekleniyor)

---

## Week 2 — Scaffolding (2026-03-27)

### Completed
- [x] `uv` package manager kuruldu (v0.11.2)
- [x] Proje `uv init` ile başlatıldı
- [x] Bağımlılıklar: `deepagents`, `langgraph-cli[inmem]`, `langchain-google-genai`, `python-dotenv`, `gitpython`, `faiss-cpu`, `langchain-community`
- [x] Deep Agent implement edildi — `agents/deep_agent/agent.py` (`create_deep_agent`)
- [x] Deep Agent araçları: `find_local_repos`, `clone_and_read_repo`, `read_local_repo`, `read_repo_file`
- [x] `langgraph.json` oluşturuldu
- [x] `.env` konfigüre edildi — `GOOGLE_API_KEY` (Paid tier 1, 10K RPD)
- [x] `gh` CLI v2.68.1 kuruldu → `C:\Users\Alperen Kayım\.local\bin\gh.exe`
- [x] `uv` + `gh` Windows user PATH'e kalıcı eklendi
- [x] `gh auth login` tamamlandı (GitHub: alperenkayim)
- [x] `langgraph dev` test edildi — port 2024, LangGraph Studio bağlantısı
- [x] Agent test edildi — `clone_and_read_repo` ile GitHub repoları başarıyla analiz edildi
- [x] Instructor `amirkiarafiei` collaborator daveti gönderildi

---

## Week 1 — Setup

### Completed
- [x] Git & GitHub hazır
- [x] VS Code + Copilot extension kuruldu
- [x] Gemini Code Assist (Antigravity) kuruldu
- [x] MCP servers: `langchain-docs`, `deepwiki`
- [x] LaTeX ortamı (research paper için)

---

## Upcoming

| Hafta | Hedef |
|-------|-------|
| Week 4 | Frontend özelleştirme (repo URL input, gelişmiş UI) |
| Later | SWE-QA dataset evaluation — her iki agent benchmark |
| Final | Research paper — mimari karşılaştırması |
