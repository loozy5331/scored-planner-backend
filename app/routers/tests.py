from fastapi import APIRouter

router = APIRouter()

@router.get("/test")
def get_response():
    return {"status": "success"}