from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config import settings
from database import get_db
from models.user import User
from schemas.user import UserRegisterRequest, UserLoginRequest, UserResponse

router = APIRouter(prefix="/api/auth", tags=["认证"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _create_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expire_minutes)
    payload = {"sub": user_id, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def _set_auth_cookie(response: JSONResponse, token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=not settings.debug,
        samesite="lax",
        max_age=settings.jwt_expire_minutes * 60,
        path="/",
    )


@router.post("/register")
async def register(req: UserRegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == req.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="邮箱已注册")

    user = User(
        email=req.email,
        password_hash=pwd_context.hash(req.password),
    )
    db.add(user)
    await db.flush()
    await db.refresh(user)

    token = _create_token(user.id)
    response = JSONResponse(
        content={"user": UserResponse.model_validate(user).model_dump()}
    )
    _set_auth_cookie(response, token)
    return response


@router.post("/login")
async def login(req: UserLoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == req.email))
    user = result.scalar_one_or_none()
    if not user or not pwd_context.verify(req.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="邮箱或密码错误")

    token = _create_token(user.id)
    response = JSONResponse(
        content={"user": UserResponse.model_validate(user).model_dump()}
    )
    _set_auth_cookie(response, token)
    return response


@router.post("/logout")
async def logout():
    response = JSONResponse(content={"message": "已退出"})
    response.delete_cookie(key="access_token", path="/")
    return response
