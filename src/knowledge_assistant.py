"""
Knowledge Assistant
Classe principale qui orchestre le système RAG
"""

from pathlib import Path
from typing import Optional, Dict, Any
from .config import Config
from .obsidian_loader import ObsidianLoader
from .vector_store import VectorStoreManager
from .rag_chain import RAGChain


class KnowledgeAssistant:
    """Classe principale du Knowledge Assistant"""
    
    def __init__(self, config: Config):
        """
        Initialise le Knowledge Assistant
        
        Args:
            config: Objet de configuration
        """
        self.config = config
        
        # Initialiser les composants
        self.loader = ObsidianLoader(
            vault_path=config.obsidian_vault_path,
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap
        )
        
        use_ollama = config.llm_provider == "ollama"
        ollama_base_url = getattr(config, 'ollama_base_url', 'http://localhost:11434')
        
        self.vector_store_manager = VectorStoreManager(
            store_path=config.vector_store_path,
            embedding_model=config.embedding_model,
            openai_api_key=config.openai_api_key,
            use_ollama=use_ollama,
            ollama_base_url=ollama_base_url
        )
        
        self.rag_chain: Optional[RAGChain] = None
        self.is_initialized = False
    
    def initialize(self, force_rebuild: bool = False) -> bool:
        """
        Initialise le système (charge ou construit la base vectorielle)
        
        Args:
            force_rebuild: Force la reconstruction de la base vectorielle
            
        Returns:
            True si succès
        """
        print("🚀 Initialisation du Knowledge Assistant...")
        
        # Essayer de charger la base vectorielle existante
        if not force_rebuild and self.vector_store_manager.load_vector_store():
            print("✅ Base vectorielle existante chargée")
        else:
            print("🔨 Construction d'une nouvelle base vectorielle...")
            self._build_vector_store()
        
        # Initialiser la chaîne RAG
        self._initialize_rag_chain()
        
        self.is_initialized = True
        print("✅ Knowledge Assistant initialisé avec succès !")
        return True
    
    def _build_vector_store(self):
        """Construit la base vectorielle depuis le vault Obsidian"""
        # Charger les documents
        documents = self.loader.load_documents()
        
        if not documents:
            raise ValueError("Aucun document trouvé dans le vault Obsidian")
        
        # Créer et sauvegarder la base vectorielle
        self.vector_store_manager.create_vector_store(documents)
        self.vector_store_manager.save_vector_store()
    
    def _initialize_rag_chain(self):
        """Initialise la chaîne RAG"""
        use_ollama = self.config.llm_provider == "ollama"
        ollama_base_url = getattr(self.config, 'ollama_base_url', 'http://localhost:11434')
        
        self.rag_chain = RAGChain(
            vector_store=self.vector_store_manager.vector_store,
            model_name=self.config.llm_model,
            temperature=self.config.llm_temperature,
            max_tokens=self.config.max_tokens,
            top_k=self.config.top_k_results,
            openai_api_key=self.config.openai_api_key,
            use_ollama=use_ollama,
            ollama_base_url=ollama_base_url
        )
    
    def ask(self, question: str, include_scores: bool = True) -> Dict[str, Any]:
        """
        Pose une question au knowledge assistant
        
        Args:
            question: Question de l'utilisateur
            include_scores: Inclure les scores de similarité
            
        Returns:
            Dictionnaire avec la réponse et les métadonnées
        """
        if not self.is_initialized:
            raise RuntimeError("Knowledge Assistant non initialisé. Appelez initialize() d'abord.")
        
        if include_scores:
            return self.rag_chain.query_with_scores(question)
        else:
            return self.rag_chain.query(question)
    
    def rebuild_index(self):
        """Reconstruit l'index de la base vectorielle"""
        print("🔄 Reconstruction de l'index de la base vectorielle...")
        self.vector_store_manager.clear_vector_store()
        self._build_vector_store()
        self._initialize_rag_chain()
        print("✅ Index reconstruit avec succès !")
    
    def get_vault_stats(self) -> Dict[str, Any]:
        """Obtient les statistiques du vault Obsidian"""
        return self.loader.get_vault_stats()
    
    def get_vector_store_stats(self) -> Dict[str, Any]:
        """Obtient les statistiques de la base vectorielle"""
        return self.vector_store_manager.get_stats()
    
    def search_documents(self, query: str, k: int = 5) -> list:
        """
        Recherche des documents pertinents
        
        Args:
            query: Requête de recherche
            k: Nombre de résultats
            
        Returns:
            Liste de documents pertinents
        """
        if not self.is_initialized:
            raise RuntimeError("Knowledge Assistant non initialisé")
        
        docs_and_scores = self.vector_store_manager.similarity_search(query, k=k)
        
        results = []
        for doc, score in docs_and_scores:
            results.append({
                'content': doc.page_content,
                'source': doc.metadata.get('source', 'Inconnu'),
                'score': float(score),
                'metadata': doc.metadata
            })
        
        return results
    
    def update_system_prompt(self, new_prompt: str):
        """
        Met à jour le template de prompt système
        
        Args:
            new_prompt: Nouveau template de prompt
        """
        if self.rag_chain:
            self.rag_chain.update_prompt(new_prompt)
    
    def get_status(self) -> Dict[str, Any]:
        """Obtient le statut du système"""
        return {
            'initialized': self.is_initialized,
            'vault_path': str(self.config.obsidian_vault_path),
            'vault_stats': self.get_vault_stats() if self.is_initialized else {},
            'vector_store_stats': self.get_vector_store_stats() if self.is_initialized else {},
            'config': {
                'llm_model': self.config.llm_model,
                'embedding_model': self.config.embedding_model,
                'top_k': self.config.top_k_results
            }
        }