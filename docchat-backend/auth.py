from fastapi import FastAPI, Header, Request
from firebase_admin_init import *  # Initializes Firebase Admin

app = FastAPI()

@app.get("/")
def home():
    return {"message": "DocChat API running ✅"}

@app.get("/verify-user")
def verify_user(authorization: str = Header(...)):
    # Expecting "Bearer <token>"
    token = authorization.split(" ")[1]
    user = verify_token(token)
    return {"uid": user["uid"], "email": user.get("email")}


def verify_token(token):
    # verification logic
    return True