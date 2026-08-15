import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.core.ports import ITokenService
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.services.token_service import TokenService

logger = logging.getLogger(__name__)

security = HTTPBearer()


def get_token_service() -> ITokenService:
    return TokenService()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
    token_service: ITokenService = Depends(get_token_service),
) -> User:
    token = credentials.credentials
    try:
        payload = token_service.decode_token(token)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            logger.warning("Token tidak memiliki claim 'sub'")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token tidak valid",
            )
    except JWTError as e:
        logger.error(f"JWT decode gagal: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token tidak valid atau expired",
        )

    user_repo = UserRepository(db)
    user = user_repo.get_by_id(int(user_id))
    if user is None:
        logger.warning(f"User dengan ID {user_id} tidak ditemukan di database")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User tidak ditemukan",
        )

    user.role = payload.get("role", "user")

    logger.info(f"User {user.email} berhasil diidentifikasi (role: {user.role})")

    return user
