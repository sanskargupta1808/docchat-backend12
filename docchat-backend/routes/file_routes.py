from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from services.text_extractor import extract_text_from_pdf
from services.rag_engine import add_document_chunks
from database import get_db
from models.document import Document
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await file.read()
    extracted_text = extract_text_from_pdf(contents, filename=file.filename)

    # ✅ Check if this filename is already stored
    existing = db.query(Document).filter(Document.filename == file.filename).first()
    if existing:
        # Still embed into vector store (maybe server restarted)
        add_document_chunks(existing.content)
        return {
            "filename": file.filename,
            "status": "Already uploaded (re-embedded)",
            "preview": existing.content[:300]
        }

    # ✅ Otherwise, store and embed
    doc = Document(filename=file.filename, content=extracted_text)
    db.add(doc)
    db.commit()

    add_document_chunks(extracted_text)

    return {
        "filename": file.filename,
        "status": "Uploaded and Processed",
        "preview": extracted_text[:300]
    }


@router.get("/")
def list_files(db: Session = Depends(get_db)):
    docs = db.query(Document).all()
    return [
        {
            "id": doc.id,
            "name": doc.filename,
            "uploaded_at": doc.uploaded_at.strftime("%Y-%m-%dT%H:%M:%S") if doc.uploaded_at else ""
        } for doc in docs
    ]


@router.delete("/files/{file_id}")
def delete_file(file_id: int, db: Session = Depends(get_db)):
    file = db.query(Document).filter(Document.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    db.delete(file)
    db.commit()
    return {"detail": "File deleted successfully"}


@router.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).all()
    return JSONResponse([
        {
            "filename": doc.filename,
            "preview": doc.content[:250] + ("..." if len(doc.content) > 250 else ""),
            "metadata": {
                "uploaded_at": doc.uploaded_at.isoformat() if doc.uploaded_at else None,
                "pages": doc.content.count("\n\n") or 1
            }
        }
        for doc in docs
    ])