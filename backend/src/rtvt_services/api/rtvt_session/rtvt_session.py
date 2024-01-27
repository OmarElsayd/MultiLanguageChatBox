import logging
import secrets
import string

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy import and_, or_, desc
from sqlalchemy.orm import Session

from rtvt_services.api.util.email_service import send_email
from rtvt_services.api.util.util import verify_invitee, init_transcript_body
from rtvt_services.db_engine.session import get_session
from rtvt_services.db_models.models import RtvtUsers, RtvtSessions, Transcripts
from rtvt_services.dependency.exception_handler import raise_http_exception
from rtvt_services.dependency.role_checker import user_pass
from rtvt_services.security_auth.jwt_auth import get_hashed_password
from rtvt_services.util.constant import NUM_SESSION_CODE_CHAR, API_V1_BASE_ROOT, CHAT_INVITATION_TEMPLATE, \
    CHAT_INVITATION_SUBJECT
from rtvt_services.util.payloads import SessionPayload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RTVT SESSION API")

router = APIRouter(
    prefix=f"{API_V1_BASE_ROOT}/session",
    tags=["session"],
    responses={
        404: {"description": "Not found"}
    }
)


@router.put(
    "/new_session",
    status_code=status.HTTP_200_OK,
    response_class=JSONResponse
)
async def start_chat_session(
        session_payload: SessionPayload,
        user: RtvtUsers = Depends(user_pass),
        db_session: Session = Depends(get_session)
):
    db_invitee = await verify_invitee(db_session, session_payload, user)
    transcript_body = init_transcript_body(session_payload, user)

    try:
        new_transcript = Transcripts(body=transcript_body)
        db_session.add(new_transcript)
        db_session.commit()

        new_session = RtvtSessions(
            user_id=user.id,
            participants=[user.user_name, session_payload.invitee],
            session_passcode=get_hashed_password(session_payload.passcode),
            is_call=session_payload.is_call,
            session_code=generate_session_id(),
            transcript_id=new_transcript.id
        )

        db_session.add(new_session)
        db_session.commit()

        send_email(
            to_email=db_invitee.email,
            template=CHAT_INVITATION_TEMPLATE,
            subject=CHAT_INVITATION_SUBJECT,
            INVITEE_NAME=db_invitee.first_name,
            CHAT_CODE=new_session.session_code,
            DATE_TIME=new_session.created_at.strftime("%H:%M %m/%d/%Y"),
            INVITER_NAME=user.first_name,
            INVITER_EMAIL=user.email
        )
        return {
            "status_code": 200,
            "session_code": new_session.session_code
        }

    except HTTPException as error:
        db_session.rollback()
        logger.error(error)
        raise_http_exception(error)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_class=JSONResponse
)
def get_all_sessions(
        page: int = Query(1, description="Page number, default is 1"),
        pagesize: int = Query(5, description="Items per page, default is 5"),
        user: RtvtUsers = Depends(user_pass),
        db_session: Session = Depends(get_session)
):
    try:
        sessions_list = (
            db_session.query(RtvtSessions).filter(
                or_(
                    user.id == RtvtSessions.user_id,
                    RtvtSessions.participants.contains([user.user_name])
                )
            )
            .order_by(desc(RtvtSessions.created_at))
            .limit(pagesize)
            .offset((page - 1) * pagesize)
            .all()
        )
        if not sessions_list:
            not_found_mess = {"message": "No sessions were found"}
            logger.info(not_found_mess)
            return HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=not_found_mess
            )
        total_count = db_session.query(RtvtSessions).count()
        return {
            "status_code": status.HTTP_200_OK,
            "total_count": total_count,
            "session_list": sessions_list
        }
    except HTTPException as error:
        logger.error(error)
        raise_http_exception(error)


# @router.put(
#     "/{session_code}/end",
#     status_code=status.HTTP_200_OK,
#     response_class=JSONResponse,
#     dependencies=[Depends(user_pass)]
# )
# def end_session(session_code: str, db_session: Session = Depends(get_session)):
#     try:
#         _session = db_session.query(RtvtSessions).filter(
#             RtvtSessions.session_code == session_code
#         ).first()
#         if _session.end_at:
#             mes = "Session has already ended"
#             logger.debug(mes)
#             raise_http_exception(mes)
#         _session.end_at = datetime.utcnow()
#         db_session.commit()

#         return {
#             "status_code": status.HTTP_200_OK
#         }
#     except HTTPException as error:
#         logger.error(error)
#         raise_http_exception(error)


@router.get(
    "/{session_code}/history",
    status_code=status.HTTP_200_OK,
    response_class=JSONResponse,
    dependencies=[Depends(user_pass)]
)
def get_session_history(
        session_code: str,
        db_session: Session = Depends(get_session)
):
    try:
        result = (
            db_session.query(Transcripts)
            .join(RtvtSessions, Transcripts.id == RtvtSessions.transcript_id)
            .filter(RtvtSessions.session_code == session_code)
            .first()
        )

        if result:
            return {
                "status_code": status.HTTP_200_OK,
                "transcript": result.body
            }

    except HTTPException as error:
        logger.error(error)
        raise_http_exception(error)


def generate_session_id(length: int = NUM_SESSION_CODE_CHAR) -> str:
    characters = string.ascii_letters + string.digits
    session_id = ''.join(secrets.choice(characters) for _ in range(length))
    return session_id


@router.get(
    '/{session_code}/info',
    status_code=status.HTTP_200_OK,
    response_class=JSONResponse
)
def get_session_info(
        session_code: str,
        db_session: Session = Depends(get_session),
        user: RtvtUsers = Depends(user_pass)
):
    try:
        participants_list = db_session.query(RtvtSessions.participants, RtvtSessions.is_call).filter(
            and_(
                RtvtSessions.session_code == session_code,
                RtvtSessions.participants.contains([user.user_name])
            )
        ).first()
        return_dict = {'is_call': participants_list[1]}
        participants_list = [name for name in participants_list[0] if name != user.user_name]
        participant_user_name = participants_list[0]

        participant_info = db_session.query(
            RtvtUsers.first_name,
            RtvtUsers.last_name,
            RtvtUsers.id,
            RtvtUsers.user_name,
        ).filter(
            RtvtUsers.user_name == participant_user_name
        ).first()

        return_dict.update(participant_info._mapping)  # pylint: disable=W0212
        return return_dict
    except HTTPException as error:
        logger.error(error)
        raise_http_exception(error)
