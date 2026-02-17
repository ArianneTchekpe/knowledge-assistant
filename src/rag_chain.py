"""
RAG Chain Implementation
Handles retrieval-augmented generation with LangChain
"""

from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.docstore.document import Document


class RAGChain:
    """Chaîne RAG pour les questions-réponses"""
    
    DEFAULT_PROMPT_TEMPLATE = """Answer the question using the context below. Be direct and conversational - just explain it naturally without mentioning documents or sources.

Context:
{context}

Question: {question}

Answer directly and naturally:"""
    
    def __init__(
        self,
        vector_store,
        model_name: str = "llama3.1",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        top_k: int = 5,
        openai_api_key: Optional[str] = None,
        use_ollama: bool = True,
        ollama_base_url: str = "http://localhost:11434"
    ):
        """
        Initialise la chaîne RAG
        
        Args:
            vector_store: Base vectorielle FAISS
            model_name: Nom du modèle
            temperature: Température du LLM
            max_tokens: Nombre maximum de tokens dans la réponse
            top_k: Nombre de documents à récupérer
            openai_api_key: Clé API OpenAI (si use_ollama=False)
            use_ollama: Utiliser Ollama au lieu d'OpenAI
            ollama_base_url: URL de base d'Ollama
        """
        self.vector_store = vector_store
        self.top_k = top_k
        
        # Initialize LLM based on provider
        if use_ollama:
            print(f"🦙 Using Ollama for LLM: {model_name}")
            self.llm = OllamaLLM(
                model=model_name,
                temperature=temperature,
                base_url=ollama_base_url,
                num_predict=max_tokens
            )
        else:
            print(f"🤖 Utilisation d'OpenAI pour le LLM : {model_name}")
            self.llm = ChatOpenAI(
                model=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                api_key=openai_api_key
            )
        
        # Créer le prompt
        self.prompt = ChatPromptTemplate.from_template(self.DEFAULT_PROMPT_TEMPLATE)
        
        # Créer la chaîne
        self.chain = (
            {"context": self._format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
    
    def _format_docs(self, question: str) -> str:
        """Formate les documents récupérés"""
        docs = self.vector_store.similarity_search(question, k=self.top_k)
        
        context_parts = []
        for i, doc in enumerate(docs, 1):
            source = doc.metadata.get('source', 'Inconnu')
            context_parts.append(f"[Document {i} - {source}]\n{doc.page_content}\n")
        
        return "\n".join(context_parts)
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Interroge le système RAG
        
        Args:
            question: Question de l'utilisateur
            
        Returns:
            Dictionnaire avec la réponse et les métadonnées
        """
        # Récupérer les documents
        docs = self.vector_store.similarity_search(question, k=self.top_k)
        
        # Générer la réponse
        answer = self.chain.invoke(question)
        
        response = {
            'answer': answer,
            'source_documents': docs,
            'sources': self._format_sources(docs),
            'usage': {
                'total_tokens': 0,
                'prompt_tokens': 0,
                'completion_tokens': 0,
                'total_cost': 0.0
            }
        }
        
        return response
    
    def query_with_scores(self, question: str) -> Dict[str, Any]:
        """
        Interroge avec les scores de similarité
        
        Args:
            question: Question de l'utilisateur
            
        Returns:
            Dictionnaire avec réponse, sources et scores
        """
        # Obtenir les documents pertinents avec scores
        docs_and_scores = self.vector_store.similarity_search_with_score(
            question, k=self.top_k
        )
        
        # Formater le contexte
        context = self._format_context(docs_and_scores)
        
        # Générer la réponse
        prompt_text = self.DEFAULT_PROMPT_TEMPLATE.format(context=context, question=question)
        answer = self.llm.invoke(prompt_text)
        
        response = {
            'answer': answer,
            'source_documents': [doc for doc, _ in docs_and_scores],
            'scores': [float(score) for _, score in docs_and_scores],
            'sources': self._format_sources_with_scores(docs_and_scores),
            'usage': {
                'total_tokens': 0,
                'prompt_tokens': 0,
                'completion_tokens': 0,
                'total_cost': 0.0
            }
        }
        
        return response
    
    def _format_context(self, docs_and_scores: List[tuple]) -> str:
        """Format documents into context string - no document labels"""
        context_parts = []
        for i, (doc, score) in enumerate(docs_and_scores, 1):
            # Just add the content without document references
            context_parts.append(doc.page_content)
        
        return "\n\n".join(context_parts)
    
    def _format_sources(self, documents: List[Document]) -> List[Dict[str, Any]]:
        """Formate les documents sources pour l'affichage"""
        sources = []
        seen = set()
        
        for doc in documents:
            source = doc.metadata.get('source', 'Inconnu')
            if source not in seen:
                sources.append({
                    'source': source,
                    'file_name': doc.metadata.get('file_name', 'Inconnu'),
                    'tags': doc.metadata.get('tags', []),
                    'links': doc.metadata.get('links', [])
                })
                seen.add(source)
        
        return sources
    
    def _format_sources_with_scores(self, docs_and_scores: List[tuple]) -> List[Dict[str, Any]]:
        """Formate les documents sources avec scores"""
        sources = []
        
        for doc, score in docs_and_scores:
            sources.append({
                'source': doc.metadata.get('source', 'Inconnu'),
                'file_name': doc.metadata.get('file_name', 'Inconnu'),
                'score': float(score),
                'tags': doc.metadata.get('tags', []),
                'links': doc.metadata.get('links', []),
                'preview': doc.page_content[:200] + '...' if len(doc.page_content) > 200 else doc.page_content
            })
        
        return sources
    
    def update_prompt(self, template: str):
        """
        Met à jour le template de prompt
        
        Args:
            template: Nouveau template de prompt
        """
        self.prompt = ChatPromptTemplate.from_template(template)
        
        # Recréer la chaîne avec le nouveau prompt
        self.chain = (
            {"context": self._format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )