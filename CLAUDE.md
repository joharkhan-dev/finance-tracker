# CLAUDE.md — Project Context & Roadmap

> Drop this file in the root of `my-finance-app/`. It gives Claude Code full context instantly, saving tokens on every session.

---

## 🎯 Goal

Turn this Google Sheets-backed AI finance tracker into a polished **portfolio piece** for AI engineering / FinTech job applications. Then deploy publicly. Then do the same for the EdTech tool.

---

## 📁 Project: my-finance-app

### What it does (working end-to-end today)
- **AI entry flow** (`app.py:56–160`): Natural language input → Gemini 2.5 Flash parses → structured JSON → saves to Google Sheets. Demo mode shows fake confirmation without writing real data.
- **Manual entry form** (sidebar, `app.py:165–176`): Date picker, category dropdown, description, amount → save to Google Sheets.
- **Dashboard tab** (`tab1`): Date range filter, 3 metric cards (income, expenses, net balance), savings rate slider with save/spend split.
- **Manage Data tab** (`tab2`): Full data table, delete a transaction by row number.
- **User filter** (sidebar, `app.py:169`): Filter dashboard by Me / Partner / Joint.

### Architecture
Google Sheets as serverless DB + Gemini AI + Streamlit frontend. Smart approach for a first project.

---

## 🐛 Bugs to Fix (ordered by severity)

| # | Bug | Location | Severity |
|---|-----|----------|----------|
| 1 | Charts hidden when balance is **positive** — pie/bar only render when `net_balance < 0` | `app.py:255–275` | 🔴 Critical (live-demo killer) |
| 2 | `NameError` crash on **empty Google Sheet** — `total_income`/`total_expense` defined inside `if not df.empty` but used outside | `app.py:234`, line 198 | 🔴 Critical |
| 3 | `NameError` on Spending Trend & Recent Transactions with **empty data** — `filtered_df` defined inside `if not df.empty` but referenced outside | `app.py:282`, `app.py:385` | 🔴 Critical |
| 4 | **Category mismatch** between AI and manual form — AI uses [Transport, Bills, Shopping, Entertainment, Health, Income]; form uses [Food, Travel, Salary, Rent, Entertainment, Other] | `app.py:69`, `app.py:169` | 🟠 High |
| 5 | **Double success toast** on manual form save — `save_data()` shows `st.success()` AND the form shows `st.success("Saved!")` | `app.py:96`, `app.py:170` | 🟡 Medium |
| 6 | `st.experimental_rerun()` removed in Streamlit 1.27+ — crashes `app_local.py` immediately | `app_local.py:139` | 🟡 Medium (local only) |
| 7 | **CRITICAL SECURITY: Real credentials committed to git** — `.streamlit/secrets.toml` has live Gemini API key and GCP service account private key | repo root | 🔴 Critical |

---

## 🚀 Improvements Roadmap (ranked by impact vs effort)

| Rank | Improvement | Impact | Effort |
|------|-------------|--------|--------|
| 1 | Fix bugs 1–3 above (charts hidden, NameError crashes, category mismatch) | Eliminates demo-killing failures | 30 min |
| 2 | **Secure credentials** — rotate keys, add `.streamlit/` to `.gitignore`, use Streamlit Cloud Secrets UI | Prevents security incident | 15 min |
| 3 | **AI confirmation step** — show parsed result for user to review/edit *before* saving | Makes AI feel agentic & trustworthy | 1–2 hrs |
| 4 | **Professional visual redesign** — dark-finance theme (dark navy/gold), custom CSS card components, animated metric deltas, logo | Biggest single perception upgrade: "student project" → "portfolio showpiece" | 2–4 hrs |
| 5 | **AI spending insights panel** — after loading data, send summary to Gemini, display short written commentary ("You spent 40% more on food this month") as a card | Demonstrates agentic AI reasoning, not just parsing | 2–3 hrs |
| 6 | **Pin `requirements.txt` versions**, add missing deps (`google-auth`, `google-api-python-client`) | Prevents silent breakage on Streamlit Cloud | 15 min |
| 7 | **Monthly breakdown view** — group by month, show month-over-month delta metrics | Adds real analytical depth | 2–3 hrs |
| 8 | **Budget alerts** — set per-category limits, show progress bar + warning when approaching limit | Practical feature, shows product thinking | 2–3 hrs |
| 9 | **Export to CSV** — single download button in Manage Data tab | Common user request, trivial to add | 20 min |
| 10 | **Rename entry point** to `streamlit_app.py` or add `[tool.streamlit]` config | Clean cloud deployment | 5 min |

---

## 🚢 Deployment Readiness

**Status: NOT READY — 4 blockers**

### Blocker 1 — Credentials in the repo (CRITICAL, do first)
1. Revoke and rotate both keys immediately in Google Cloud Console
2. Add `.streamlit/secrets.toml` to `.gitignore`
3. Set secrets in Streamlit Cloud dashboard (Settings → Secrets) using same TOML format — `st.secrets` works identically, zero code changes needed

### Blocker 2 — No entry point configuration
Streamlit Cloud defaults to `streamlit_app.py`. Either rename `app.py` → `streamlit_app.py`, or in Streamlit Cloud deploy settings, explicitly set main file path to `app.py`.

### Blocker 3 — `requirements.txt` has no versions
Add minimum versions:
```
streamlit>=1.40.0
pandas>=2.0
plotly>=5.0
gspread>=6.0
oauth2client>=4.1.3
google-generativeai>=0.8.0
```
Note: `oauth2client` is deprecated — replace with `google-auth`. `google-generativeai` SDK has breaking changes across versions — pin it.

### Blocker 4 — `finance.db` and `app_local.py` pollute the repo
Streamlit Cloud filesystem is ephemeral — writes to `finance.db` are lost on restart. Since the app correctly uses Google Sheets, these files serve no purpose in the deployed version. Move them or add to `.gitignore`.

### Non-blockers worth noting
- `.python-version` specifies 3.9; Streamlit Cloud supports it but 3.11+ is recommended for performance
- `_lessons/` directory is committed — fine for portfolio repo, but adds noise

---

## 📋 Session Workflow (for Claude Code)

When starting a new session, read this file first, then tackle the next unchecked item below:

### Phase 1 — Security & Stability (do before ANY git push)
- [ ] **Rotate credentials** — revoke Gemini key + GCP service account key in Google Cloud Console
- [ ] Add `.streamlit/secrets.toml` to `.gitignore` and verify it's no longer tracked (`git rm --cached .streamlit/secrets.toml`)
- [ ] Fix Bug 1: Charts hidden when balance positive (`app.py:255–275`) — move chart render outside `else` block
- [ ] Fix Bug 2: NameError on empty sheet — initialise `total_income = 0`, `total_expense = 0` before the `if not df.empty` block
- [ ] Fix Bug 3: NameError on Spending Trend / Recent Transactions — initialise `filtered_df = pd.DataFrame()` before the `if not df.empty` block
- [ ] Fix Bug 4: Unify category lists between AI prompt and manual form
- [ ] Fix Bug 5: Remove duplicate success toast
- [ ] Fix Bug 6: Replace `st.experimental_rerun()` with `st.rerun()` in `app_local.py`
- [ ] Pin `requirements.txt` versions + replace `oauth2client` with `google-auth`
- [ ] Rename `app.py` → `streamlit_app.py` OR set entry point in Streamlit Cloud settings
- [ ] Add `finance.db`, `app_local.py`, `_lessons/` to `.gitignore` (or decide to keep lessons for portfolio)

### Phase 2 — Portfolio Polish
- [x] AI confirmation step — `st.session_state["pending_tx"]` stores parse result; green-bordered review card with editable fields; Confirm & Save / Cancel buttons; `st.toast` persists through rerun (`finance_app.py:125–200`)
- [ ] Professional visual redesign — dark navy/gold theme, custom CSS cards
- [ ] AI spending insights panel
- [ ] Monthly breakdown view
- [ ] Budget alerts
- [ ] Export to CSV button
- [ ] **Receipt / photo upload** — file uploader accepts image; Gemini Vision reads receipt and auto-fills the confirmation card (same `pending_tx` flow); do after Supabase migration

### Phase 3 — Deploy
- [ ] Set Streamlit Cloud secrets
- [ ] Deploy and smoke-test with empty sheet, then with real data
- [ ] Make repo public (after confirming no secrets remain)

### Phase 4 — EdTech Tool
- [ ] EdTech tool uses **Supabase** as its backend (Postgres, not Google Sheets)
- [ ] Consider migrating finance app from Google Sheets → Supabase for consistency, better scalability, real SQL queries, and easier auth. Worth evaluating before deep investment in the Sheets architecture.
- [ ] (Add EdTech project details here when ready)

---

## 🗂 Key File Map

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit app (cloud version, uses Google Sheets) |
| `app_local.py` | Local version with SQLite — buggy, not for deployment |
| `finance_app_v1.py` | Old version — ignore |
| `setup_db.py` | SQLite setup — only relevant for `app_local.py` |
| `finance.db` | SQLite DB — not used in cloud version, shouldn't be committed |
| `.streamlit/secrets.toml` | 🔴 Contains live credentials — must NEVER be pushed to git |
| `requirements.txt` | Dependencies — needs version pins |
| `my_tracker.csv` | Data export — probably shouldn't be committed |
| `_lessons/` | Learning exercises — separate from the app |

---

## 💼 Job Application Context

- Target roles: AI engineering, FinTech
- This is a **first project** — the concept and AI integration are legitimately impressive
- Bugs 1–3 would cause visible failures within 60 seconds of a live demo → fix these first
- The four changes that transform this: fix bugs → secure credentials → visual redesign → AI insights panel
- Once deployed: add live URL to CV/LinkedIn/portfolio

---

*Last updated: April 2026 — based on Claude Code audit*
