# 🧠 Obsidian Knowledge Assistant

Transform your Obsidian vault into an intelligent, queryable knowledge base using RAG. 100% local and free!

## ✨ Features

- 🔍 Semantic Search - AI-powered note finding
- 💬 Intelligent Q&A - Context-aware answers
- 📚 Source Attribution - See which notes were used
- 🔒 100% Local - Your data stays private
- 💰 Free - No API costs with Ollama

## 🚀 Quick Start

### 1. Install Ollama
Download from https://ollama.com/download

```bash
ollama pull llama3.2:1b
ollama pull nomic-embed-text
```

### 2. Install Dependencies
```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### 3. Configure
```bash
copy .env.example .env  # Windows
cp .env.example .env    # Mac/Linux
# Edit .env with your vault path
```

### 4. Run
```bash
python -m streamlit run app.py
```

## 📖 Example Questions

- "What is a Python decorator?"
- "Explain neural networks"
- "Summarize my notes about [topic]"

## ⚙️ Configuration

Edit `.env`:
```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2:1b
OBSIDIAN_VAULT_PATH=./examples/sample_vault
```

## 🔧 Troubleshooting

**"Model requires more memory"** → Use `llama3.2:3b`
**"Ollama connection failed"** → Start Ollama app
**"No documents found"** → Check vault path in `.env`

## 📊 Model Options

- `llama3.2:1b` - 1.5 GB RAM (recommended)
- `llama3.2:3b` - 3 GB RAM
- `llama3.1` - 8 GB RAM

---

Made with ❤️ using LangChain • FAISS • Ollama • Streamlit