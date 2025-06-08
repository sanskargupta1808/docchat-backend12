# vector_store.py
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from database import SessionLocal
from models.document import Document

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize FAISS index (dimension must match embedding size)
embedding_dim = 384
index = faiss.IndexFlatL2(embedding_dim)

# Store mapping from index -> (doc_id, chunk)
doc_chunks = []

def embed_and_index_documents():
    session = SessionLocal()
    documents = session.query(Document).all()
    for doc in documents:
        text = doc.preview
        chunks = split_text(text)
        for chunk in chunks:
            embedding = embedder.encode(chunk)
            index.add(np.array([embedding]).astype("float32"))
            doc_chunks.append((doc.id, chunk))
    session.close()

def search_similar_chunks(query, top_k=3):
    query_embedding = embedder.encode(query).astype("float32").reshape(1, -1)
    D, I = index.search(query_embedding, top_k)
    return [doc_chunks[i][1] for i in I[0] if i < len(doc_chunks)]

def split_text(text, max_length=200):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]