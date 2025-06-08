from sqlalchemy.orm import Session
from models.document import Document

def save_document_to_db(db: Session, filename: str, content: str):
    doc = Document(filename=filename, content=content)
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc