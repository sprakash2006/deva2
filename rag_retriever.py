import os
import logging
import chromadb
from sentence_transformers import SentenceTransformer
from langchain_core.documents import Document
from openai import OpenAI

class RAGRetriever:
    def __init__(self, api_key: str, persist_dir="rag_store", top_k=5):
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")

        # Initialize Chroma persistent client
        self.client = chromadb.PersistentClient(path=persist_dir)

        # Create or get the Chroma collection
        self.collection = self.client.get_or_create_collection(
            name="deva_docs",
            metadata={"hnsw:space": "cosine"}
        )

        self.top_k = top_k
        self.gpt = OpenAI(api_key=api_key)

    def query(self, question: str) -> str:
        try:
            query_embed = self.embedder.encode(question).tolist()

            results = self.collection.query(
                query_embeddings=[query_embed],
                n_results=self.top_k
            )

            if not results["documents"] or not results["documents"][0]:
                return "🤖 Sorry, I couldn't find anything relevant in the uploaded documents."

            context = "\n".join(results["documents"][0])

            prompt = f"""
You are DEVA — a helpful AI with access to user documents.
Use the context to answer accurately. If answer not found,
say politely that context lacks that information.

Context:
{context}

Question:
{question}
"""

            response = self.gpt.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.4
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            logging.error(f"RAG query failed: {e}", exc_info=True)
            return f"⚠️ RAG Error: {e}"

    def add_documents(self, user_id: str, filename: str, chunks: list[str]):
        if not chunks:
            logging.warning("No chunks provided to add_documents()")
            return

        try:
            metadatas = [{"user_id": user_id, "source": filename}] * len(chunks)
            ids = [f"{user_id}_{filename}_{i}" for i in range(len(chunks))]

            self.collection.add(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
            logging.info(f"✅ Added {len(chunks)} chunks to Chroma for {user_id} ({filename})")
        except Exception as e:
            logging.error(f"❌ Failed to add documents: {e}", exc_info=True)
