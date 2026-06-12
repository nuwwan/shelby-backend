from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schema.auth_user import AuthUserCreate, AuthUserResponse, LoginUser
from app.controllers.auth_user import register_user, login_user

router = APIRouter(prefix="/auth", tags=["auth"])

# register route
@router.post("/register", response_model=AuthUserResponse, status_code=status.HTTP_201_CREATED)
def register_route(payload: AuthUserCreate, db: Session = Depends(get_db)):
    return register_user(db, payload)

# login route
@router.post("/login")
def login_route(payload: LoginUser, db: Session = Depends(get_db)):
    return login_user(db, payload)

# # logout route
# @router.post("/logout")
# def logout_route(logout: Logout, db: Session = Depends(get_db)):
#     return logout(db, logout)

# # refresh token route
# @router.post("/refresh-token")
# def refresh_token_route(refresh_token: RefreshToken, db: Session = Depends(get_db)):
#     return refresh_token(db, refresh_token)

# # verify token route
# @router.post("/verify-token")
# def verify_token_route(verify_token: VerifyToken, db: Session = Depends(get_db)):
#     return verify_token(db, verify_token)

# # reset password route
# @router.post("/reset-password")
# def reset_password_route(reset_password: ResetPassword, db: Session = Depends(get_db)):
#     return reset_password(db, reset_password)

# # verify email route
# @router.post("/verify-email")
# def verify_email_route(verify_email: VerifyEmail, db: Session = Depends(get_db)):
#     return verify_email(db, verify_email)

# # delete account route  
# @router.delete("/delete-account")
# def delete_account_route(delete_account: DeleteAccount, db: Session = Depends(get_db)):
#     return delete_account(db, delete_account)