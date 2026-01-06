from typing import List, Optional
import io
import os
from pathlib import Path
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.docstore.document import Document as LangchainDocument
import chromadb
from chromadb.config import Settings

from config import settings


class RAGService:
    """Serviço para Retrieval-Augmented Generation"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(openai_api_key=settings.openai_api_key)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Diretórios locais para armazenamento
        self.base_dir = Path(__file__).parent.parent / "storage"
        self.pdf_dir = self.base_dir / "pdfs"
        self.chroma_dir = self.base_dir / "chroma_db"
        
        # Criar diretórios se não existirem
        self.pdf_dir.mkdir(parents=True, exist_ok=True)
        self.chroma_dir.mkdir(parents=True, exist_ok=True)
        
        # ChromaDB persistente em arquivo local
        self.chroma_client = chromadb.PersistentClient(
            path=str(self.chroma_dir),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
    async def extract_text_from_pdf(self, pdf_file: bytes) -> tuple[str, int]:
        """
        Extrai texto de um arquivo PDF
        
        Returns:
            tuple: (texto_completo, numero_de_paginas)
        """
        try:
            pdf_reader = PdfReader(io.BytesIO(pdf_file))
            total_pages = len(pdf_reader.pages)
            
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text, total_pages
        except Exception as e:
            raise ValueError(f"Erro ao processar PDF: {str(e)}")
    
    def chunk_text(self, text: str, metadata: dict = None) -> List[LangchainDocument]:
        """
        Divide o texto em chunks menores para embedding
        """
        if metadata is None:
            metadata = {}
            
        documents = [LangchainDocument(page_content=text, metadata=metadata)]
        chunks = self.text_splitter.split_documents(documents)
        
        return chunks
    
    async def create_embeddings(self, chunks: List[LangchainDocument], collection_name: str) -> Chroma:
        """
        Cria embeddings dos chunks e armazena no ChromaDB
        """
        try:
            vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embeddings,
                collection_name=collection_name,
                client=self.chroma_client
            )
            return vectorstore
        except Exception as e:
            raise ValueError(f"Erro ao criar embeddings: {str(e)}")
    
    async def similarity_search(
        self, 
        query: str, 
        collection_name: str, 
        k: int = 3
    ) -> List[LangchainDocument]:
        """
        Busca os chunks mais relevantes para a query
        
        Args:
            query: Pergunta do usuário
            collection_name: Nome da coleção no ChromaDB
            k: Número de chunks para retornar
            
        Returns:
            Lista de documentos relevantes
        """
        try:
            vectorstore = Chroma(
                collection_name=collection_name,
                embedding_function=self.embeddings,
                client=self.chroma_client
            )
            
            results = vectorstore.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"Erro na busca: {str(e)}")
            return []
    
    def format_context_for_llm(self, documents: List[LangchainDocument]) -> str:
        """
        Formata os documentos recuperados em um contexto para o LLM
        """
        if not documents:
            return ""
        
        context = "Contexto dos documentos:\n\n"
        for i, doc in enumerate(documents, 1):
            context += f"Trecho {i}:\n{doc.page_content}\n\n"
        
        return context
    
    def save_pdf_file(self, pdf_file: bytes, user_id: str, filename: str) -> str:
        """
        Salva o PDF fisicamente no disco local
        
        Returns:
            str: Caminho relativo do arquivo salvo
        """
        # Criar diretório do usuário
        user_dir = self.pdf_dir / user_id
        user_dir.mkdir(exist_ok=True)
        
        # Gerar nome único para o arquivo
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        safe_filename = f"{unique_id}_{filename}"
        file_path = user_dir / safe_filename
        
        # Salvar arquivo
        with open(file_path, "wb") as f:
            f.write(pdf_file)
        
        return str(file_path.relative_to(self.base_dir))
    
    def delete_pdf_file(self, file_path: str):
        """Deleta o PDF do disco"""
        try:
            full_path = self.base_dir / file_path
            if full_path.exists():
                full_path.unlink()
        except Exception as e:
            print(f"Erro ao deletar arquivo: {e}")
    
    async def process_pdf_for_rag(
        self, 
        pdf_file: bytes, 
        filename: str,
        user_id: str,
        conversation_id: Optional[str] = None
    ) -> dict:
        """
        Pipeline completo: salva PDF, extrai texto, cria chunks e embeddings
        
        Returns:
            dict com informações do processamento
        """
        # 1. Salvar PDF no disco
        saved_path = self.save_pdf_file(pdf_file, user_id, filename)
        
        # 2. Extrair texto
        text, total_pages = await self.extract_text_from_pdf(pdf_file)
        
        # 3. Criar chunks
        metadata = {
            "filename": filename,
            "user_id": user_id,
            "conversation_id": conversation_id or "general",
            "file_path": saved_path
        }
        chunks = self.chunk_text(text, metadata)
        
        # 4. Criar collection name único
        collection_name = f"user_{user_id}_{conversation_id or 'general'}"
        
        # 5. Criar embeddings (persistidos no disco via ChromaDB)
        await self.create_embeddings(chunks, collection_name)
        
        return {
            "filename": filename,
            "total_pages": total_pages,
            "total_chunks": len(chunks),
            "collection_name": collection_name,
            "file_path": saved_path,
            "message": "PDF processado e salvo localmente com sucesso"
        }
    
    def delete_collection(self, collection_name: str):
        """Deleta uma coleção do ChromaDB"""
        try:
            self.chroma_client.delete_collection(collection_name)
        except Exception as e:
            print(f"Erro ao deletar coleção: {e}")


# Instância global do serviço RAG
rag_service = RAGService()

