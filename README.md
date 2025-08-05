# 🧠 commit-intel

> LLM-powered local Git commit review CLI tool for Android engineers.

`commit-intel` runs a local AI agent pipeline using [Ollama](https://ollama.com) and [LangGraph](https://github.com/langchain-ai/langgraph) to review staged or committed code diffs, providing feedback on:

- 🔍 Summary
- 🧪 Code critique
- 💡 Suggestions
- 🔐 Security issues
- 📐 Architecture
- 🧪 Test coverage
- 🖼️ UI changes (Jetpack Compose or XML)
- 📦 Dependency usage
- ⚡ Performance
- 🔤 Readability

---

## ✅ Features (Phase 1–2 Complete)

### ✅ Local-first
- Uses [Ollama](https://ollama.com) and local models like `codellama:7b` (no cloud API calls required)

### ✅ CLI Tool
- Run via simple terminal commands:
  ```bash
  review commit
  review commit --diff HEAD~2
  review staged
  ```

### ✅ Git Pre-commit Hook
- Optional hook setup:
  ```bash
  review install-prehook
  ```

### ✅ Multi-agent LangGraph Review Pipeline
- Diff is passed through a LangGraph of LLM-powered agents in sequence
- Skips agents that are not applicable (e.g., no UI or test files)

---

## 📦 Installation

1. Clone the repo:
   ```bash
   cd commit-intel
   ```

2. Set up a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

3. Pull the model using Ollama:
   ```bash
   ollama pull codellama:7b
   ```

4. Run the CLI:
   ```bash
   review --help
   ```

---

## 💻 Example Output

```bash
review commit

🧠 Commit Summary:
- Updated login flow to use new auth provider
- Removed legacy authentication code

🧪 Critique:
- Missing error handling for network failure
- Redundant logging in auth callback

💡 Suggestions:
- Extract token parsing into a separate function
```

---

## 📁 Project Structure

```
commit-intel/
├── cli/                # Typer CLI entrypoints
├── core/               # LangGraph, Ollama, agents
├── .pre-commit/        # Hook logic
├── tests/              # Unit tests (TBD)
└── README.md
```

---

## 🔮 Future Improvements (Phase 3+)

- ✅ Export feedback to Markdown (`--markdown`)
- ✅ CLI flags to enable/disable agents
- ⚙️ Gradle plugin integration
- 📈 Coverage integration from JaCoCo reports
- 🔁 Streaming token-based output
- 🔧 Model config via `.commit-intel.yml`
- 🧠 Model fallback: use OpenAI if Ollama is down
- 🛠️ Workspace scoring: code quality % per commit
- 🧪 Automated fix suggestions (optional auto PRs)

---

## 🧠 Credits

Built by Android engineers, for Android engineers.  
Inspired by LangChain, LangGraph, Ollama, and open-source LLM tooling.

MIT License.
