"""
Streamlit Web Interface for Knowledge Assistant
"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

from src.config import Config
from src.knowledge_assistant import KnowledgeAssistant

# Page configuration
st.set_page_config(
    page_title="Obsidian Knowledge Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS - Modern Professional Design
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
.main { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); background-attachment: fixed; }
.block-container { padding: 2rem; background: white; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); margin: 1rem; }
.main-header { font-size: 3.5rem; font-weight: 700; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-align: center; margin-bottom: 1rem; letter-spacing: -1px; }
.subtitle { text-align: center; color: #6b7280; font-size: 1.2rem; margin-bottom: 2rem; font-weight: 400; }
.example-prompts { background: linear-gradient(135deg, #f6f8fb 0%, #e9ecf5 100%); border-radius: 15px; padding: 1.5rem; margin: 1rem 0 2rem 0; border: 1px solid #e2e8f0; }
.example-prompts h3 { color: #1e293b; font-size: 1.3rem; font-weight: 600; margin-bottom: 1rem; }
.prompt-card { background: white; border-radius: 10px; padding: 1rem 1.2rem; margin: 0.8rem 0; border-left: 4px solid #667eea; box-shadow: 0 2px 8px rgba(0,0,0,0.08); transition: all 0.3s ease; cursor: pointer; }
.prompt-card:hover { transform: translateX(5px); box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2); }
.source-card { background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); border-left: 4px solid #667eea; border-radius: 12px; padding: 1.2rem; margin: 0.8rem 0; box-shadow: 0 4px 12px rgba(0,0,0,0.08); transition: all 0.3s ease; }
.source-card:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15); }
.stat-box { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3); }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #1e293b 0%, #334155 100%); }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label { color: white !important; }
.stButton > button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border: none; border-radius: 10px; padding: 0.6rem 1.5rem; font-weight: 600; transition: all 0.3s ease; }
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4); }
</style>
""", unsafe_allow_html=True)

# Example prompts
EXAMPLE_PROMPTS = {
    "🐍 Python": [
        "What is a Python decorator?",
        "What are Python best practices?",
        "How does a decorator work?",
    ],
    "🤖 Machine Learning": [
        "What is supervised learning?",
        "Explain neural networks",
        "What are classification metrics?",
        "Difference between MSE and RMSE?",
    ],
    "📚 General": [
        "Summarize all my notes",
        "What topics have I studied?",
        "What did I learn about programming?",
    ]
}

@st.cache_resource
def load_assistant():
    try:
        config = Config()
        assistant = KnowledgeAssistant(config)
        return assistant, None
    except Exception as e:
        return None, str(e)

def initialize_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'assistant_initialized' not in st.session_state:
        st.session_state.assistant_initialized = False
    if 'total_queries' not in st.session_state:
        st.session_state.total_queries = 0
    if 'current_prompt' not in st.session_state:
        st.session_state.current_prompt = ""

def display_sidebar(assistant):
    with st.sidebar:
        st.markdown("# 🧠 Knowledge Assistant")
        st.markdown("### *Powered by Ollama & FAISS*")
        st.divider()
        st.markdown("## ")
        
        if assistant and st.session_state.assistant_initialized:
            status = assistant.get_status()
            st.success("✅ System Operational")
            vault_stats = status.get('vault_stats', {})
            
            col1, col2 = st.columns(2)
            #with col1:
                #st.metric("", vault_stats.get('total_files', 0), "Indexed")
            #with col2:
                #st.metric("💾 Size", f"{vault_stats.get('total_size_mb', 0):.1f} MB")
            
            #vs_stats = status.get('vector_store_stats', {})
            #st.metric("📚 Chunks", vs_stats.get('num_documents', 0), "Indexed")
           # st.divider()
            
            with st.expander("⚙️ Configuration"):
                config_info = status.get('config', {})
                st.markdown(f"**LLM:** `{config_info.get('llm_model', 'N/A')}`  \n**Embeddings:** `{config_info.get('embedding_model', 'N/A')}`")
            
            st.divider()
            st.markdown("## 🔧 Actions")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Rebuild", use_container_width=True):
                    with st.spinner("Rebuilding..."):
                        try:
                            assistant.rebuild_index()
                            st.success("✅ Done!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ {e}")
            with col2:
                if st.button(" Clear", use_container_width=True):
                    st.session_state.messages = []
                    st.rerun()
        else:
            st.warning("⚠️ Not Initialized")
        
        st.divider()
        st.markdown("## 📈 Session")
        st.metric("💬 Queries", st.session_state.total_queries, "Total")

def display_example_prompts():
    st.markdown('<div class="example-prompts"><h3>💡 Try these questions</h3></div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for idx, (category, prompts) in enumerate(EXAMPLE_PROMPTS.items()):
        with cols[idx % 3]:
            st.markdown(f"**{category}**")
            for prompt in prompts:
                if st.button(prompt, key=f"p_{category}_{prompt}", use_container_width=True):
                    st.session_state.current_prompt = prompt
                    st.rerun()

def display_chat_interface(assistant):
    st.markdown('<h1 class="main-header">💬 Ask Your Knowledge Base</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Get answers from your Obsidian notes</p>', unsafe_allow_html=True)
    
    if len(st.session_state.messages) == 0:
        display_example_prompts()
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar="🧑‍💻" if message["role"] == "user" else "🤖"):
            st.markdown(message["content"])
            if message["role"] == "assistant" and "sources" in message:
                with st.expander("📚 Sources"):
                    for source in message["sources"]:
                        st.markdown(f'<div class="source-card"><strong>📄 {source["file_name"]}</strong><br>Score: {source.get("score", 0):.4f}</div>', unsafe_allow_html=True)
    
    if prompt := st.chat_input("💭 Ask your question..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)
        
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("🤔 Searching..."):
                try:
                    response = assistant.ask(prompt, include_scores=True)
                    st.markdown(response['answer'])
                    st.session_state.messages.append({"role": "assistant", "content": response['answer'], "sources": response['sources']})
                    with st.expander("📚 Sources", expanded=True):
                        for source in response['sources']:
                            st.markdown(f'<div class="source-card"><strong>📄 {source["file_name"]}</strong><br>Score: {source.get("score", 0):.4f}<br>{source.get("preview", "")[:200]}</div>', unsafe_allow_html=True)
                    st.session_state.total_queries += 1
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ {e}")

def main():
    initialize_session_state()
    assistant, error = load_assistant()
    
    if error:
        st.error(f"❌ Failed to load: {error}")
        st.stop()
    
    if not st.session_state.assistant_initialized:
        with st.spinner("🚀 Initializing..."):
            try:
                assistant.initialize()
                st.session_state.assistant_initialized = True
                st.success("✅ Ready!")
            except Exception as e:
                st.error(f"❌ {e}")
                st.stop()
    
    display_sidebar(assistant)
    tab1, tab2 = st.tabs(["💬 Chat", "ℹ️ About"])
    
    with tab1:
        display_chat_interface(assistant)
    
    with tab2:
        st.markdown('<h1 class="main-header">ℹ️ About</h1>', unsafe_allow_html=True)
        st.markdown("""
        
        
        ##  Technologies
        - **LangChain** - RAG orchestration
        - **FAISS** - Vector database
        - **Ollama** - Local AI models
        - **Streamlit** - Web interface
        
        <div style='text-align: center; padding: 2rem; color: #64748b;'>
        Created with ❤️<br><small>LangChain • FAISS • Ollama • Streamlit</small>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()