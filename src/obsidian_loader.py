"""
Chargeur de documents Obsidian
Gère le chargement et le parsing des fichiers markdown
"""

import re
from pathlib import Path
from typing import List, Dict, Any
import frontmatter
from langchain_community.docstore.document import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ObsidianLoader:
    """Chargeur pour les fichiers markdown Obsidian"""
    
    def __init__(self, vault_path: Path, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialise le chargeur Obsidian
        
        Args:
            vault_path: Chemin vers le vault Obsidian
            chunk_size: Taille des chunks de texte
            chunk_overlap: Chevauchement entre les chunks
        """
        self.vault_path = Path(vault_path)
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
    
    def load_documents(self) -> List[Document]:
        """
        Charge tous les documents markdown du vault Obsidian
        
        Returns:
            Liste d'objets Document
        """
        documents = []
        
        if not self.vault_path.exists():
            raise ValueError(f"Le chemin du vault n'existe pas : {self.vault_path}")
        
        # Trouver tous les fichiers markdown
        markdown_files = list(self.vault_path.rglob("*.md"))
        
        print(f"📁 Trouvé {len(markdown_files)} fichiers markdown dans le vault")
        
        for md_file in markdown_files:
            try:
                docs = self._load_single_file(md_file)
                documents.extend(docs)
            except Exception as e:
                print(f"⚠️ Erreur lors du chargement de {md_file.name}: {e}")
        
        print(f"✅ Chargé {len(documents)} chunks de documents")
        return documents
    
    def _load_single_file(self, file_path: Path) -> List[Document]:
        """
        Charge et traite un seul fichier markdown
        
        Args:
            file_path: Chemin vers le fichier markdown
            
        Returns:
            Liste de chunks Document
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parser le frontmatter
        post = frontmatter.loads(content)
        metadata = dict(post.metadata)
        text = post.content
        
        # Extraire les métadonnées supplémentaires
        metadata['source'] = str(file_path.relative_to(self.vault_path))
        metadata['file_name'] = file_path.stem
        metadata['file_path'] = str(file_path)
        
        # Extraire les liens wiki
        wiki_links = self._extract_wiki_links(text)
        if wiki_links:
            metadata['links'] = wiki_links
        
        # Extraire les tags
        tags = self._extract_tags(text)
        if tags:
            metadata['tags'] = tags
        
        # Nettoyer le markdown
        cleaned_text = self._clean_markdown(text)
        
        # Découper en chunks
        chunks = self.text_splitter.create_documents(
            texts=[cleaned_text],
            metadatas=[metadata]
        )
        
        return chunks
    
    def _extract_wiki_links(self, text: str) -> List[str]:
        """
        Extrait les liens wiki style Obsidian [[lien]]
        
        Args:
            text: Texte markdown
            
        Returns:
            Liste des noms de notes liées
        """
        pattern = r'\[\[([^\]]+)\]\]'
        links = re.findall(pattern, text)
        # Supprimer les alias (texte après |)
        links = [link.split('|')[0] for link in links]
        return list(set(links))
    
    def _extract_tags(self, text: str) -> List[str]:
        """
        Extrait les tags du texte markdown
        
        Args:
            text: Texte markdown
            
        Returns:
            Liste des tags
        """
        # Correspond au format #tag
        pattern = r'#(\w+)'
        tags = re.findall(pattern, text)
        return list(set(tags))
    
    def _clean_markdown(self, text: str) -> str:
        """
        Nettoie le formatage markdown pour un meilleur traitement
        
        Args:
            text: Texte markdown brut
            
        Returns:
            Texte nettoyé
        """
        # Supprimer les liens wiki mais garder le texte
        text = re.sub(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', r'\2', text)
        text = re.sub(r'\[\[([^\]]+)\]\]', r'\1', text)
        
        # Supprimer les espaces excessifs
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        # Supprimer les commentaires markdown
        text = re.sub(r'%%.*?%%', '', text, flags=re.DOTALL)
        
        return text.strip()
    
    def get_vault_stats(self) -> Dict[str, Any]:
        """
        Obtient des statistiques sur le vault
        
        Returns:
            Dictionnaire avec les statistiques
        """
        markdown_files = list(self.vault_path.rglob("*.md"))
        
        total_size = sum(f.stat().st_size for f in markdown_files)
        
        return {
            'total_files': len(markdown_files),
            'total_size_mb': total_size / (1024 * 1024),
            'vault_path': str(self.vault_path)
        }