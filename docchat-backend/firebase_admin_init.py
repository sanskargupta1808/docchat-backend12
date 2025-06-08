import firebase_admin
from firebase_admin import credentials, auth
import os
from dotenv import load_dotenv

load_dotenv()

# Load credentials from service account JSON path in .env
cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIAL_PATH"))
firebase_admin.initialize_app(cred)