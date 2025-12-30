import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import os

class VectorManager:
    def __init__(self, collection_name="rag_collection"):
        self.client = chromadb.PersistentClient(path="./data/chroma_db")
        
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
        self.collection = self.client.get_or_create_collection(
            name=collection_name, 
            embedding_function=self.embedding_fn
        )

    def chunk_text(self, text, chunk_size=500, overlap=100):
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += (chunk_size - overlap)
        return chunks

    def add_documents(self, documents):
        all_chunks = []
        ids = []
        for i, doc in enumerate(documents):
            chunks = self.chunk_text(doc)
            for j, chunk in enumerate(chunks):
                all_chunks.append(chunk)
                ids.append(f"doc_{i}_chunk_{j}")
        
        if all_chunks:
            self.collection.add(
                documents=all_chunks,
                ids=ids
            )

    def query(self, text, n_results=3):
        results = self.collection.query(
            query_texts=[text],
            n_results=n_results
        )
        return results["documents"][0] if results["documents"] else []
