from fastapi import APIRouter

router = APIRouter()

@router.get("/settings")
def get_settings():
    return {
        "theme": "dark",
        "notifications": True,
        "language": "en"
    }