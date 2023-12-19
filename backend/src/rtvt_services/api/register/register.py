import logging

from rtvt_services.security_auth.jwt_auth import get_hashed_password
from rtvt_services.util.payloads import SignupOutput, UserInput
from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import or_

from ...db_engine.session import get_session
from ...db_models.models import Role, RtvtUsers

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Register logging")

router = APIRouter(
    prefix="/signup",
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
        new_user = RtvtUsers(**creds_form.model_dump(), role=Role.User)
        session.add(new_user)
        session.commit()

        return SignupOutput(status_code=status.HTTP_200_OK)

    except HTTPException as error:
        if error.status_code == 400:
            raise error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error"
        )


async def find_user(creds_form, session):

    is_user = (
        session.query(RtvtUsers)
        .filter(
            or_(
                RtvtUsers.user_name == creds_form.user_name,
                RtvtUsers.email == creds_form.email
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