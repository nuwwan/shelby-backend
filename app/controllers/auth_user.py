from sqlalchemy.orm import Session
from app.models.auth_user import AuthUser
from app.schema.auth_user import AuthUserCreate, AuthUserUpdate, LoginUser
from app.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException


def register_user(db: Session, register: AuthUserCreate) -> AuthUser:
    """Register a new user and return the created record."""
    # 1. Make sure all required fields were provided.
    if not register.email or not register.password or not register.name:
        raise HTTPException(
            status_code=400, detail="Email, password and name are required"
        )

    # 2. Reject the request if the email is already taken (email must be unique).
    existing_user = (
        db.query(AuthUser).filter(AuthUser.email == register.email).first()
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # 3. Hash the password — never store the raw password in the database.
    hashed_password = hash_password(register.password)

    # 4. Build the user record with the hashed password.
    db_auth_user = AuthUser(
        name=register.name,
        email=register.email,
        password=hashed_password,
    )

    # 5. Save it, then refresh to load DB-generated fields (id, timestamps).
    db.add(db_auth_user)
    db.commit()
    db.refresh(db_auth_user)

    # 6. Return the newly created user.
    return db_auth_user


def login_user(db: Session, login: LoginUser):
    """Authenticate a user with email + password and return an access token."""
    # 1. Make sure credentials were provided.
    if not login.email or not login.password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    # 2. Look up the user by email.
    db_auth_user = db.query(AuthUser).filter(AuthUser.email == login.email).first()

    # 3. Verify the user exists and the password matches.
    #    Use one generic message so we don't reveal which emails are registered.
    if not db_auth_user or not verify_password(login.password, db_auth_user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # 4. Block inactive accounts from logging in.
    if not db_auth_user.is_active:
        raise HTTPException(status_code=403, detail="Account is inactive")

    # 5. Issue a signed JWT access token (the user id is stored in the token's "sub").
    access_token = create_access_token(subject=db_auth_user.id)

    # 6. Return the token to the client.
    return {"access_token": access_token, "token_type": "bearer"}