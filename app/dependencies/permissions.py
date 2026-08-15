from fastapi import Depends, HTTPException, status

from app.core.permissions import ROLE_PERMISSIONS
from app.dependencies.auth import get_current_user
from app.models.user_model import User


def require_permission(permission: str):
    def permission_checker(current_user: User = Depends(get_current_user)):
        user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])
        if permission not in user_permissions:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Tidak memiliki akses",
            )
        return current_user
    return permission_checker
