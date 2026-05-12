from fastapi import APIRouter


router = APIRouter()

@router.get('/')
def health_check():
  return {
    "health": "I am, alive."
  }