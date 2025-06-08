from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.rag_engine import query_gpt

router = APIRouter()

class ChatRequest(BaseModel):
    query: str

@router.post("/chat")
def chat_query(request: ChatRequest):
    try:
        response = query_gpt(request.query)
        return {"query": request.query, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))