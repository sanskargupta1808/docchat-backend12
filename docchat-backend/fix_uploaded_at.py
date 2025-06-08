# fix_uploaded_at.py
from database import SessionLocal
from models.document import Document
from datetime import datetime

db = SessionLocal()
docs = db.query(Document).filter(Document.uploaded_at == None).all()

for doc in docs:
    doc.uploaded_at = datetime.utcnow()

db.commit()
db.close()
print(f"✅ Fixed {len(docs)} records with missing uploaded_at")