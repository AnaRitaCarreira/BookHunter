from fastapi import Depends, APIRouter
from auth import get_current_user
from models.user import User

router = APIRouter()

@router.get("/users/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {"username": current_user.username}
