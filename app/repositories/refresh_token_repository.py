from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.refresh_token_model import RefreshToken


class RefreshTokenRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, user_id: int, token: str, expires_at: datetime) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at,
        )
        self.db.add(refresh_token)
        self.db.commit()
        self.db.refresh(refresh_token)
        return refresh_token

    def get_by_token(self, token: str) -> RefreshToken | None:
        return self.db.query(RefreshToken).filter(RefreshToken.token == token).first()

    def revoke_all_for_user(self, user_id: int) -> None:
        self.db.query(RefreshToken).filter(
            RefreshToken.user_id == user_id,
            RefreshToken.revoked == False,
        ).update({"revoked": True})
        self.db.commit()

    def revoke(self, token: str) -> None:
        self.db.query(RefreshToken).filter(RefreshToken.token == token).update(
            {"revoked": True}
        )
        self.db.commit()

    def is_valid(self, token: str) -> bool:
        refresh_token = self.get_by_token(token)
        if not refresh_token:
            return False
        if refresh_token.revoked:
            return False
        if refresh_token.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
            return False
        return True
