import logging
import os

from fastapi.responses import JSONResponse
from fastapi import APIRouter, status, Depends, HTTPException

from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.orm import Session
from sqlalchemy import or_

from mlcb_services.api.util.email_service import send_email
from mlcb_services.security_auth.jwt_auth import get_hashed_password
from mlcb_services.util.payloads import SignupOutput, UserInput
from mlcb_services.db_engine.session import get_session
from mlcb_services.db_models.models import Role, MlcbUsers
from mlcb_services.util.constant import (
    API_V1_BASE_ROOT,
    EMAIL_CONFIRMATION_TEMPLET,
    EMAIL_CONFIRMATION_SUBJECT
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Register logging")

router = APIRouter(
    prefix=f"{API_V1_BASE_ROOT}/signup",
    tags=["signup"],
    responses={
        404: {"description": "Not found"}
    }
)


@router.put(
    "",
    status_code=status.HTTP_200_OK,
    response_model=SignupOutput
)
async def sign_up(creds_form: UserInput, session: Session = Depends(get_session)):
    try:
        await find_user(creds_form, session)

        creds_form.password = get_hashed_password(creds_form.password)
        new_user = MlcbUsers(**creds_form.model_dump(), role=Role.User)
        session.add(new_user)

        send_email(
            to_email=creds_form.email,
            template=EMAIL_CONFIRMATION_TEMPLET,
            FIRST_NAME=creds_form.first_name,
            CONFIRMATION_CODE=generate_confirmation_token(creds_form.email),
            subject=EMAIL_CONFIRMATION_SUBJECT
        )
        session.commit()

        return SignupOutput(status_code=status.HTTP_200_OK)

    except HTTPException as error:
        if error.status_code == 400:
            raise error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


@router.post(
    "/conf_email",
    status_code=status.HTTP_200_OK,
    response_class=JSONResponse
)
async def conf_email(token: str, session: Session = Depends(get_session)):
    try:
        email = confirm_token(token)
        if not email:
            raise HTTPException(status_code=400, detail="Invalid or expired token")

        user = session.query(MlcbUsers).filter(MlcbUsers.email == email).first()

        if not user:
            logger.error("Can not find user in the database")
            raise HTTPException(status_code=500, detail="Contact your admin")

        user.is_confirmed = True
        session.commit()

        return {
            "status_code": status.HTTP_200_OK
        }
    except HTTPException as error:
        logger.error(error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


async def find_user(creds_form, session):
    is_user = (
        session.query(MlcbUsers)
        .filter(
            or_(
                MlcbUsers.user_name == creds_form.user_name,
                MlcbUsers.email == creds_form.email
            )
        )
        .first()
    )

    if not is_user:
        return

    logger.info(is_user.user_name)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Account already exist"
    )


def generate_confirmation_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(os.getenv("JWT_SECRET_KEY"))
    return serializer.dumps(email, salt=os.getenv("SECRET_SALT"))


def confirm_token(token: str, expiration=3600) -> str:
    serializer = URLSafeTimedSerializer(os.getenv("JWT_SECRET_KEY"))
    return serializer.loads(
        token,
        salt=os.getenv("SECRET_SALT"),
        max_age=expiration
    )
