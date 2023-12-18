import json
import logging

from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from jose import jwt

from rtvt_services.db_engine.session import get_session
from rtvt_services.db_models.models import RtvtUsers
from rtvt_services.security_auth.jwt_auth import JwtAuth
from rtvt_services.util.constant import ALGORITHM
from rtvt_services.util.payloads import TokenPayload, InCompingTokenPayload


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("User dep logger")

OAuthSchema = OAuth2PasswordBearer(
    tokenUrl="/login",
    scheme_name="JWT",
)
jwt_auth = JwtAuth()


async def get_curr_user(token: str = Depends(OAuthSchema), session: Session = Depends(get_session)):
    try:
        logger.info(token)
        payload_dict = jwt.decode(
            token, jwt_auth.JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )

        token_data = TokenPayload(**payload_dict)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_data = InCompingTokenPayload(**json.loads(token_data.sub.replace("'", '"')))
        logger.info(user_data)

    except jwt.JWTError as error:
        logger.error(error)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Could not validate credentials {error}",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return validate_user(session, user_data)


def validate_user(session, user_data):
    try:
        user = session.query(RtvtUsers).filter(RtvtUsers.id == user_data.id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"}
            )
        return user

    except Exception as error:
        logger.error(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
