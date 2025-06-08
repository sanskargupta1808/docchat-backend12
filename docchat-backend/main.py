from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import file_routes, chat_routes, analytics_routes, user_routes
from services.rag_engine import preload_documents
import os

app = FastAPI()

# ✅ Load all documents into FAISS on startup
@app.on_event("startup")
def load_faiss_index():
    preload_documents()

# ✅ CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use specific origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register routers
app.include_router(file_routes.router, prefix="/files", tags=["Files"])
app.include_router(chat_routes.router, prefix="/chat", tags=["Chat"])
app.include_router(analytics_routes.router, prefix="/analytics", tags=["Analytics"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])

# ✅ Health check route
@app.get("/")
def read_root():
    return {"message": "DocChat Backend is Live!"}