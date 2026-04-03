from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.hash import hash_password, verify_password
from app.utils.jwt import create_access_token, create_refresh_token

def register_user(db: Session, data):
    user = User(
        username=data.username,
        email=data.email,
        password=hash_password(data.password),
        role="author"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(db, data):
    username = data["username"]
    password = data["password"]

    user = db.query(User).filter(User.username == username).first()

    if not user or not verify_password(password, user.password):
        return None

    return {
        "access_token": create_access_token({"user_id": user.id, "role": user.role}),
        "refresh_token": create_refresh_token({"user_id": user.id})
    }