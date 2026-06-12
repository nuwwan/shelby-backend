from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema.auth_user import AuthUserCreate, AuthUserUpdate, AuthUserResponse
from app.controllers.auth_user import create_auth_user, get_auth_user, get_all_auth_users, update_auth_user, delete_auth_user

router = APIRouter(prefix="/auth", tags=["auth"])

# @router.post("/users")
# def create_auth_user_route(auth_user: AuthUserCreate, db: Session = Depends(get_db)):
#     return create_auth_user(db, auth_user)

# @router.get("/users/{auth_user_id}")
# def get_auth_user_route(auth_user_id: str, db: Session = Depends(get_db)):
#     return get_auth_user(db, auth_user_id)

# @router.get("/users")
# def get_all_auth_users_route(db: Session = Depends(get_db)):
#     return get_all_auth_users(db)

# @router.put("/users/{auth_user_id}")
# def update_auth_user_route(auth_user_id: str, auth_user: AuthUserUpdate, db: Session = Depends(get_db)):
#     return update_auth_user(db, auth_user_id, auth_user)

# @router.delete("/users/{auth_user_id}")
# def delete_auth_user_route(auth_user_id: str, db: Session = Depends(get_db)):
#     return delete_auth_user(db, auth_user_id)

# register route
@router.post("/register")
def register_route(register: RegisterUser, db: Session = Depends(get_db)):
    return register(db, register)

# login route
@router.post("/login")
def login_route(login: LoginUser, db: Session = Depends(get_db)):
    return login(db, login)

# logout route
@router.post("/logout")
def logout_route(logout: Logout, db: Session = Depends(get_db)):
    return logout(db, logout)

# refresh token route
@router.post("/refresh-token")
def refresh_token_route(refresh_token: RefreshToken, db: Session = Depends(get_db)):
    return refresh_token(db, refresh_token)

# verify token route
@router.post("/verify-token")
def verify_token_route(verify_token: VerifyToken, db: Session = Depends(get_db)):
    return verify_token(db, verify_token)

# reset password route
@router.post("/reset-password")
def reset_password_route(reset_password: ResetPassword, db: Session = Depends(get_db)):
    return reset_password(db, reset_password)

# verify email route
@router.post("/verify-email")
def verify_email_route(verify_email: VerifyEmail, db: Session = Depends(get_db)):
    return verify_email(db, verify_email)

# delete account route  
@router.delete("/delete-account")
def delete_account_route(delete_account: DeleteAccount, db: Session = Depends(get_db)):
    return delete_account(db, delete_account)