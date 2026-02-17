"""
Vector Store Manager
Handles FAISS operations
"""

import pickle
from pathlib import Path
from typing import List, Optional, Tuple
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_community.docstore.document import Document


class VectorStoreManager:
    """Gestionnaire pour la base vectorielle FAISS"""
    
    def __init__(
        self,
        store_path: Path,
        embedding_model: str = "nomic-embed-text",
        openai_api_key: Optional[str] = None,
        use_ollama: bool = True,
        ollama_base_url: str = "http://localhost:11434"
    ):
        """
        Initialise le gestionnaire de vector store
        
        Args:
            store_path: Chemin de stockage de la base vectorielle
            embedding_model: Nom du modèle d'embedding
            openai_api_key: Clé API OpenAI (si use_ollama=False)
            use_ollama: Utiliser Ollama au lieu d'OpenAI
            ollama_base_url: URL de base d'Ollama
        """
        self.store_path = Path(store_path)
        self.store_path.mkdir(parents=True, exist_ok=True)
        
        # Choose embeddings based on provider
        if use_ollama:
            print(f"🦙 Using Ollama for embeddings: {embedding_model}")
            self.embeddings = OllamaEmbeddings(
                model=embedding_model,
                base_url=ollama_base_url
            )
        else:
            print(f"🤖 Using OpenAI for embeddings: {embedding_model}")
            self.embeddings = OpenAIEmbeddings(
                model=embedding_model,
                openai_api_key=openai_api_key
            )
        
        self.vector_store: Optional[FAISS] = None
        self.index_path = self.store_path / "faiss_index"
        self.metadata_path = self.store_path / "metadata.pkl"
    
    def create_vector_store(self, documents: List[Document]) -> FAISS:
        """
        Crée une nouvelle base vectorielle à partir des documents
        
        Args:
            documents: Liste de documents à indexer
            
        Returns:
            Base vectorielle FAISS
        """
        if not documents:
            raise ValueError("Aucun document fourni pour l'indexation")
        
        print(f"🔨 Création de la base vectorielle à partir de {len(documents)} documents...")
        
        self.vector_store = FAISS.from_documents(
            documents=documents,
            embedding=self.embeddings
        )
        
        print("✅ Base vectorielle créée avec succès")
        return self.vector_store
    
    def save_vector_store(self):
        """Sauvegarde la base vectorielle sur disque"""
        if self.vector_store is None:
            raise ValueError("Aucune base vectorielle à sauvegarder")
        
        print(f"💾 Sauvegarde de la base vectorielle dans {self.store_path}...")
        
        # Sauvegarder l'index FAISS
        self.vector_store.save_local(str(self.index_path))
        
        # Sauvegarder les métadonnées supplémentaires
        metadata = {
            'num_documents': len(self.vector_store.docstore._dict),
            'embedding_model': getattr(self.embeddings, 'model', 'unknown')
        }
        
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(metadata, f)
        
        print("✅ Base vectorielle sauvegardée avec succès")
    
    def load_vector_store(self) -> bool:
        """
        Charge la base vectorielle depuis le disque
        
        Returns:
            True si chargée avec succès, False sinon
        """
        if not self.index_path.exists():
            print("ℹ️ Aucune base vectorielle existante trouvée")
            return False
        
        try:
            print(f"📂 Chargement de la base vectorielle depuis {self.store_path}...")
            
            self.vector_store = FAISS.load_local(
                str(self.index_path),
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            
            # Charger les métadonnées
            if self.metadata_path.exists():
                with open(self.metadata_path, 'rb') as f:
                    metadata = pickle.load(f)
                print(f"✅ Base vectorielle chargée avec {metadata.get('num_documents', 'N/A')} documents")
            
            return True
        
        except Exception as e:
            print(f"❌ Erreur lors du chargement de la base vectorielle : {e}")
            return False
    
    def add_documents(self, documents: List[Document]):
        """
        Ajoute des documents à la base vectorielle existante
        
        Args:
            documents: Documents à ajouter
        """
        if self.vector_store is None:
            raise ValueError("Base vectorielle non initialisée")
        
        print(f"➕ Ajout de {len(documents)} documents à la base vectorielle...")
        self.vector_store.add_documents(documents)
        print("✅ Documents ajoutés avec succès")
    
    def similarity_search(
        self,
        query: str,
        k: int = 5,
        score_threshold: Optional[float] = None
    ) -> List[Tuple[Document, float]]:
        """
        Recherche des documents similaires
        
        Args:
            query: Requête de recherche
            k: Nombre de résultats à retourner
            score_threshold: Score minimum de similarité
            
        Returns:
            Liste de tuples (Document, score)
        """
        if self.vector_store is None:
            raise ValueError("Base vectorielle non initialisée")
        
        # Obtenir les documents avec scores
        docs_and_scores = self.vector_store.similarity_search_with_score(query, k=k)
        
        # Filtrer par seuil de score si fourni
        if score_threshold is not None:
            docs_and_scores = [
                (doc, score) for doc, score in docs_and_scores
                if score <= score_threshold  # FAISS utilise la distance (plus bas = meilleur)
            ]
        
        return docs_and_scores
    
    def get_stats(self) -> dict:
        """
        Obtient les statistiques de la base vectorielle
        
        Returns:
            Dictionnaire avec les statistiques
        """
        if self.vector_store is None:
            return {'status': 'non_initialisée'}
        
        return {
            'status': 'initialisée',
            'num_documents': len(self.vector_store.docstore._dict),
            'embedding_model': getattr(self.embeddings, 'model', 'unknown'),
            'index_path': str(self.index_path)
        }
    
    def clear_vector_store(self):
        """Efface la base vectorielle"""
        self.vector_store = None
        
        # Supprimer les fichiers
        if self.index_path.exists():
            import shutil
            shutil.rmtree(self.index_path)
        
        if self.metadata_path.exists():
            self.metadata_path.unlink()
        
        print("🗑️ Base vectorielle effacée")