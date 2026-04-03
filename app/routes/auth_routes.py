from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.utils.time import get_ist_time
from app.database import get_db
from app.schemas.user_schema import UserCreate
from app.schemas.auth_schema import TokenResponse, RefreshTokenRequest
from app.services.auth_service import register_user, login_user
from app.utils.jwt import decode_token, create_access_token
from app.utils.time import get_ist_time
import pytz

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = register_user(db, user)
        return {
            "msg": "User registered successfully",
            "user": {
                "id": new_user.id,
                "username": new_user.username,
                "email": new_user.email,
                
            }
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"User registration failed: {str(e)}")
        
@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    result = login_user(
        db,
        {
            "username": form_data.username,
            "password": form_data.password
        }
    )

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return result

@router.post("/refresh-token")
def refresh_token(data: RefreshTokenRequest):
    try:
        payload = decode_token(data.refresh_token)

        # 🔐 Validate token type
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )

        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        new_access = create_access_token({
            "user_id": user_id,
            "role": payload.get("role")
        })

        return {
            "success": True,
            "access_token": new_access,
            "token_type": "bearer"
        }

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token"
        )