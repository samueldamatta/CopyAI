import io
import os
import uuid
from pathlib import Path
from typing import List, Optional

import chromadb
from chromadb.config import Settings
from langchain.docstore.document import Document as LangchainDocument
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from pypdf import PdfReader

from domain.gateways.rag_gateway import RAGGateway


class ChromaDBRAGGateway(RAGGateway):
    def __init__(self, openai_api_key: str, base_storage_dir: str):
        self._embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, length_function=len
        )

        self._base_dir = Path(base_storage_dir)
        self._pdf_dir = self._base_dir / "pdfs"
        self._chroma_dir = self._base_dir / "chroma_db"

        self._pdf_dir.mkdir(parents=True, exist_ok=True)
        self._chroma_dir.mkdir(parents=True, exist_ok=True)

        self._chroma_client = chromadb.PersistentClient(
            path=str(self._chroma_dir),
            settings=Settings(anonymized_telemetry=False, allow_reset=True),
        )

    async def process_pdf(
        self,
        pdf_bytes: bytes,
        filename: str,
        user_id: str,
        conversation_id: Optional[str] = None,
    ) -> dict:
        saved_path = self._save_pdf(pdf_bytes, user_id, filename)
        text, total_pages = self._extract_text(pdf_bytes)
        metadata = {
            "filename": filename,
            "user_id": user_id,
            "conversation_id": conversation_id or "general",
            "file_path": saved_path,
        }
        chunks = self._chunk_text(text, metadata)
        collection_name = f"user_{user_id}_{conversation_id or 'general'}"
        self._create_embeddings(chunks, collection_name)

        return {
            "filename": filename,
            "total_pages": total_pages,
            "total_chunks": len(chunks),
            "collection_name": collection_name,
            "file_path": saved_path,
            "message": "PDF processado e salvo localmente com sucesso",
        }

    async def search_similar(self, query: str, collection_name: str, k: int = 3) -> str:
        try:
            vectorstore = Chroma(
                collection_name=collection_name,
                embedding_function=self._embeddings,
                client=self._chroma_client,
            )
            docs = vectorstore.similarity_search(query, k=k)
            if not docs:
                return ""
            context = "Contexto dos documentos:\n\n"
            for i, doc in enumerate(docs, 1):
                context += f"Trecho {i}:\n{doc.page_content}\n\n"
            return context
        except Exception as e:
            print(f"Erro na busca RAG: {e}")
            return ""

    def delete_collection(self, collection_name: str) -> None:
        try:
            self._chroma_client.delete_collection(collection_name)
        except Exception as e:
            print(f"Erro ao deletar coleção: {e}")

    def delete_file(self, file_path: str) -> None:
        try:
            full_path = self._base_dir / file_path
            if full_path.exists():
                full_path.unlink()
        except Exception as e:
            print(f"Erro ao deletar arquivo: {e}")

    # --- private helpers ---

    def _save_pdf(self, pdf_bytes: bytes, user_id: str, filename: str) -> str:
        user_dir = self._pdf_dir / user_id
        user_dir.mkdir(exist_ok=True)
        unique_id = str(uuid.uuid4())[:8]
        safe_name = f"{unique_id}_{filename}"
        file_path = user_dir / safe_name
        file_path.write_bytes(pdf_bytes)
        return str(file_path.relative_to(self._base_dir))

    def _extract_text(self, pdf_bytes: bytes) -> tuple[str, int]:
        reader = PdfReader(io.BytesIO(pdf_bytes))
        total_pages = len(reader.pages)
        text = "".join(page.extract_text() + "\n" for page in reader.pages)
        return text, total_pages

    def _chunk_text(self, text: str, metadata: dict) -> List[LangchainDocument]:
        docs = [LangchainDocument(page_content=text, metadata=metadata)]
        return self._splitter.split_documents(docs)

    def _create_embeddings(self, chunks: List[LangchainDocument], collection_name: str) -> None:
        Chroma.from_documents(
            documents=chunks,
            embedding=self._embeddings,
            collection_name=collection_name,
            client=self._chroma_client,
        )
