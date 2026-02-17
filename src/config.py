"""
Gestionnaire de configuration
Charge et valide les variables d'environnement
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Classe de configuration pour Knowledge Assistant"""
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialise la configuration
        
        Args:
            env_file: Chemin vers le fichier .env (optionnel)
        """
        if env_file:
            load_dotenv(env_file)
        else:
            load_dotenv()
        
        # Type de LLM à utiliser
        self.llm_provider = os.getenv("LLM_PROVIDER", "ollama").lower()
        
        if self.llm_provider == "openai":
            # Configuration OpenAI
            self.openai_api_key = os.getenv("OPENAI_API_KEY")
            if not self.openai_api_key:
                raise ValueError(
                    "OPENAI_API_KEY non trouvée dans les variables d'environnement.\n"
                    "Créez un fichier .env à partir de .env.example et ajoutez votre clé API."
                )
        elif self.llm_provider == "ollama":
            # Configuration Ollama
            self.ollama_base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
            self.openai_api_key = None  # Pas besoin pour Ollama
        else:
            raise ValueError(f"LLM_PROVIDER non supporté : {self.llm_provider}")
        
        # Configuration Obsidian
        vault_path = os.getenv("OBSIDIAN_VAULT_PATH", "./obsidian_vault")
        self.obsidian_vault_path = Path(vault_path)
        
        # Configuration des modèles
        if self.llm_provider == "ollama":
            self.embedding_model = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
            self.llm_model = os.getenv("LLM_MODEL", "llama3.1")
        else:
            self.embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
            self.llm_model = os.getenv("LLM_MODEL", "gpt-4-turbo-preview")
        
        self.llm_temperature = float(os.getenv("LLM_TEMPERATURE", "0.7"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
        
        # Configuration du vector store
        self.vector_store_path = Path(os.getenv("VECTOR_STORE_PATH", "./data/vector_store"))
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "1000"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "200"))
        
        # Configuration de recherche
        self.top_k_results = int(os.getenv("TOP_K_RESULTS", "5"))
        self.similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.7"))
        
        # Configuration du cache
        self.enable_cache = os.getenv("ENABLE_CACHE", "true").lower() == "true"
        self.cache_dir = Path(os.getenv("CACHE_DIR", "./data/cache"))
        
        # Créer les répertoires nécessaires
        self._create_directories()
    
    def _create_directories(self):
        """Crée les répertoires nécessaires s'ils n'existent pas"""
        self.vector_store_path.mkdir(parents=True, exist_ok=True)
        if self.enable_cache:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def validate(self) -> bool:
        """
        Valide la configuration
        
        Returns:
            True si la configuration est valide
        """
        if not self.obsidian_vault_path.exists():
            print(f"⚠️ Le chemin du vault Obsidian n'existe pas : {self.obsidian_vault_path}")
            print(f"Veuillez vérifier la variable OBSIDIAN_VAULT_PATH dans le fichier .env")
            return False
        
        return True
    
    def __repr__(self) -> str:
        """Représentation textuelle de la configuration"""
        return f"""Config(
    LLM Provider: {self.llm_provider}
    Vault Obsidian: {self.obsidian_vault_path}
    Modèle LLM: {self.llm_model}
    Modèle Embedding: {self.embedding_model}
    Vector Store: {self.vector_store_path}
    Top K: {self.top_k_results}
)"""