# 🧠 Obsidian Knowledge Assistant

Transform your Obsidian vault into an intelligent, queryable knowledge base using RAG. 100% local and free!



##  Quick Start

### 1. Install Ollama
Download from https://ollama.com/download

```bash
ollama pull llama mistral
ollama pull nomic-embed-text
```

### 2. Install Dependencies
```bash
python -m venv .venv
.venv/Scripts/Activate.ps1  # Windows
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

##  Example Questions

- "What is a Python decorator?"
- "Explain neural networks"
- "Summarize my notes about [topic]"

##  Configuration

Edit `.env`:
```env
LLM_PROVIDER=ollama
LLM_MODEL=llama3.2:1b
OBSIDIAN_VAULT_PATH=./examples/sample_vault


Made with  using LangChain • FAISS • Ollama • Streamlit