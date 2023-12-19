import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from jose.jwt import JWTError

from rtvt_services.db_engine.session import get_session
from rtvt_services.db_models.models import RtvtUsers
from rtvt_services.dependency.role_checker import user_pass
from rtvt_services.security_auth.jwt_auth import JwtAuth, verify_users_password
from rtvt_services.util.payloads import TokenResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("login api")


router = APIRouter(
    prefix="/login",
    tags=["login"],
    responses={
        404: {"description": "Not found"}
    }
)

jwt_auth = JwtAuth()


@router.post(
    "",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(creds_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    username = creds_form.username
    user = session.query(RtvtUsers).filter(RtvtUsers.user_name == username).first()

    if not user or not verify_users_password(creds_form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password"
        )

    token_payload = {
        "id": user.id,
        "user_name": user.user_name,
    }
    try:
        token = jwt_auth.create_access_token(token_payload)

        return TokenResponse(
            status_code=status.HTTP_200_OK,
            access_token=token,
        )

    except JWTError as jwt_error:
        logger.error(jwt_error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(jwt_error)
        )


@router.get(
    "/profile"
)
async def get_info(user: RtvtUsers = Depends(user_pass)):
    return {
        "profile": user
    }
