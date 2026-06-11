from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema.auth_user import AuthUserCreate, AuthUserUpdate, AuthUserResponse
from app.controllers.auth_user import create_auth_user, get_auth_user, get_all_auth_users, update_auth_user, delete_auth_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/users")
def create_auth_user_route(auth_user: AuthUserCreate, db: Session = Depends(get_db)):
    return create_auth_user(db, auth_user)

@router.get("/users/{auth_user_id}")
def get_auth_user_route(auth_user_id: str, db: Session = Depends(get_db)):
    return get_auth_user(db, auth_user_id)

@router.get("/users")
def get_all_auth_users_route(db: Session = Depends(get_db)):
    return get_all_auth_users(db)

@router.put("/users/{auth_user_id}")
def update_auth_user_route(auth_user_id: str, auth_user: AuthUserUpdate, db: Session = Depends(get_db)):
    return update_auth_user(db, auth_user_id, auth_user)

@router.delete("/users/{auth_user_id}")
def delete_auth_user_route(auth_user_id: str, db: Session = Depends(get_db)):
    return delete_auth_user(db, auth_user_id)