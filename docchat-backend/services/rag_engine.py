from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from openai import OpenAI
import os
from langchain.text_splitter import CharacterTextSplitter
from models.document import Document
from database import SessionLocal

# Initialize SentenceTransformer model (for FAISS)
embedder = SentenceTransformer('all-MiniLM-L6-v2')

# OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# FAISS vector store
dimension = 384  # Embedding size of MiniLM
index = faiss.IndexFlatL2(dimension)
documents = []

# ✅ Add document chunks from text
def add_document_chunks(text: str):
    global documents, index

    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_text(text)

    if not chunks:
        raise ValueError("No chunks generated from text. Upload may be empty.")

    embeddings = embedder.encode(chunks)
    embeddings_array = np.array(embeddings)

    # Debugging
    print("Embedding shape:", embeddings_array.shape)
    if len(embeddings_array.shape) != 2 or embeddings_array.shape[1] != dimension:
        raise ValueError(f"Embedding shape mismatch. Expected (?, {dimension}), got {embeddings_array.shape}")

    index.add(embeddings_array)
    documents.extend(chunks)

# ✅ Preload all stored documents from DB at startup
def preload_documents():
    db = SessionLocal()
    try:
        all_docs = db.query(Document).all()
        for doc in all_docs:
            if not doc.content or doc.content.strip() == "":
                print(f"⚠️ Skipping empty document: {doc.filename}")
                continue
            try:
                add_document_chunks(doc.content)
            except Exception as e:
                print(f"❌ Failed to embed document {doc.filename}: {str(e)}")
        print(f"✅ Preloaded {len(documents)} total chunks into FAISS index")
    finally:
        db.close()

# ✅ Query GPT-4o using nearest document chunks
def query_gpt(query: str):
    if len(documents) == 0 or index.ntotal == 0:
        return "No documents have been added yet. Please upload a file first."

    query_vector = embedder.encode([query])
    query_array = np.array(query_vector)

    if query_array.shape != (1, dimension):
        return f"Invalid query vector shape: {query_array.shape}"

    D, I = index.search(query_array, k=3)
    valid_indices = [i for i in I[0] if i < len(documents)]

    if not valid_indices:
        return "No relevant information found."

    context = "\n".join([documents[i] for i in valid_indices])

    prompt = f"""You are a helpful assistant. Based on the following document context, answer the user query.

Context:
{context}

Question: {query}
Answer:"""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content