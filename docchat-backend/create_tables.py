# create_tables.py

from models import document
from database import engine

document.Base.metadata.create_all(bind=engine)
print("✅ Tables created successfully.")