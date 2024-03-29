import logging

from fastapi import Depends, HTTPException, status
from mlcb_services.db_models.models import Role, MlcbUsers
from mlcb_services.dependency.user_checker import get_curr_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Role Checker")


class RoleChecker:
    def __init__(self, allowed_roles: list):
        self.allowed_roles = allowed_roles

    def __call__(self, user: MlcbUsers = Depends(get_curr_user)):
        if user.role not in self.allowed_roles:
            logger.debug(f"User with role {user.role} not in {self.allowed_roles}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized")
        return user


admin_pass = RoleChecker([Role.Admin])
user_pass = RoleChecker([Role.User, Role.Admin])
