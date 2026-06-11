from sqlalchemy.orm import Session
from app.models.auth_user import AuthUser
from app.schema.auth_user import AuthUserCreate, AuthUserUpdate
from fastapi import HTTPException


def create_auth_user(db: Session, auth_user: AuthUserCreate):
    db_auth_user = AuthUser(name=auth_user.name, email=auth_user.email, password=auth_user.password)
    db.add(db_auth_user)
    db.commit()
    db.refresh(db_auth_user)
    return db_auth_user

def get_auth_user(db: Session, auth_user_id: str):
    return db.query(AuthUser).filter(AuthUser.id == auth_user_id).first()

def get_all_auth_users(db: Session):
    return db.query(AuthUser).all()

def update_auth_user(db: Session, auth_user_id: str, auth_user: AuthUserUpdate):
    db_auth_user = db.query(AuthUser).filter(AuthUser.id == auth_user_id).first()
    if not db_auth_user:
        raise HTTPException(status_code=404, detail="Auth user not found")
    db_auth_user.name = auth_user.name
    db_auth_user.email = auth_user.email
    db_auth_user.password = auth_user.password
    db.commit()
    db.refresh(db_auth_user)
    return db_auth_user

def delete_auth_user(db: Session, auth_user_id: str):
    db_auth_user = db.query(AuthUser).filter(AuthUser.id == auth_user_id).first()
    if not db_auth_user:
        raise HTTPException(status_code=404, detail="Auth user not found")
    db.delete(db_auth_user)
    db.commit()