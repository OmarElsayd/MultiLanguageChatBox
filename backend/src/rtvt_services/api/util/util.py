import copy
import logging
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.attributes import flag_modified
from fastapi import HTTPException, status

from rtvt_services.db_models.models import RtvtUsers, RtvtSessions, UsersSession, Transcripts
from rtvt_services.dependency.exception_handler import (
    TranslationException, DbSessionException, raise_http_exception
)
from rtvt_services.util.constant import SUPPORTED_LANGS, TRANSCRIPTS_BODY
from rtvt_services.util.payloads import SessionPayload, InComingWsMessagePayload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("API UTIL LOGGING")


def verify_session_invitation(user: RtvtUsers, db_session: Session, session_code: str):
    """

    :param user:
    :param db_session:
    :param session_code:
    :return: None if not verified
    """
    # noinspection PyTypeChecker
    return db_session.query(
        RtvtSessions
    ).filter(
        RtvtSessions.session_code == session_code
    ).filter(
        RtvtSessions.participants.contains([user.user_name])
    ).first()


def verify_supported_language(target_language_code: str):
    logger.info(target_language_code)
    if target_language_code not in SUPPORTED_LANGS:
        raise TranslationException("Unsupported Lang or wrong code")


async def update_transcript_body_text(
        session: Session,
        session_code: str,
        ws_body: InComingWsMessagePayload,
        after_translation: str,
        user: RtvtUsers
):
    try:
        transcript_body_tuple = session.query(Transcripts).join(
            RtvtSessions, RtvtSessions.transcript_id == Transcripts.id
        ).filter(
            RtvtSessions.session_code == session_code
        ).one()
        transcript_body = transcript_body_tuple.body
        user_key = next(
            (key for key, value in transcript_body['info'].items() if value == user.user_name),
            None
        )
        transcript_body["body"][user_key][user.user_name]["transcript_text"].append(
            {
                "text": {
                    "before": ws_body.content,
                    "after": after_translation
                },
                "time": ws_body.created_at
            }
        )
        flag_modified(transcript_body_tuple, "body")
        session.commit()
    except NoResultFound:
        logger.error(f"Transcript body doesn't exist for session code {session_code}")
        raise DbSessionException("Please contact your IT admin")


async def update_users_session(
        user: RtvtUsers,
        session_query: RtvtSessions,
        session: Session,
        spoken_lang: str
) -> None:
    try:
        user_session = UsersSession(
            user_id=user.id,
            session_id=session_query.id,
            spoken_lang=spoken_lang
        )
        session.add(user_session)
        session.flush()
        transcript_body_tuple = session.query(Transcripts).filter(
            Transcripts.id == session_query.transcript_id
        ).first()
        updated_transcript_body = await update_transcript_body_lang(
            transcript_body_tuple.body, spoken_lang, user
        )
        transcript_body_tuple.body = updated_transcript_body
        flag_modified(transcript_body_tuple, "body")

        logger.info(transcript_body_tuple.body)
        session.commit()
    except DbSessionException as error:
        logger.error(error)
        session.rollback()
        raise DbSessionException(error)


async def update_transcript_body_lang(transcript_body, spoken_lang, user):

    user_key = next(
        (key for key, value in transcript_body['info'].items() if value == user.user_name),
        None
    )
    logger.info(f"update_transcript_body_lang: {user_key} ")
    if not user_key:
        logger.error(
            f"Transcript body doesn't have user {user.user_name} with session code:"
        )
        raise DbSessionException("Please contact your IT admin")

    logger.info("Found user in the transcript body dict, changing user lang")
    if isinstance(transcript_body, dict):
        transcript_body["info"][user_key + "_lang"] = spoken_lang
        transcript_body['body'][user_key][user.user_name]['source_lang'] = spoken_lang
        logger.info("Changing user lang in transcript body has been done")
        return transcript_body

    logger.error("transcript_body['info'] is not a dictionary")


def init_transcript_body(session_payload: SessionPayload, user: RtvtUsers) -> dict:
    transcript_body = copy.deepcopy(TRANSCRIPTS_BODY)

    transcript_body['info']['user1'] = user.user_name
    transcript_body['info']['user2'] = session_payload.invitee
    transcript_body['body']['user1'][user.user_name] = transcript_body['body']['user1'].pop(
        "REPLACE_WITH_USER1_USERNAME"
    )
    transcript_body['body']['user2'][session_payload.invitee] = transcript_body['body']['user2'].pop(
        "REPLACE_WITH_USER2_USERNAME"
    )

    return transcript_body


async def verify_invitee(db_session, session_payload, user):
    invitee = (
        db_session.query(RtvtUsers).filter_by(
            user_name=session_payload.invitee
        ).first())

    if not invitee or user.user_name == session_payload.invitee:
        message = "Didn't find user"
        logger.info(message)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )
    return invitee


async def end_session(session_code: str, db_session: Session) :
    _session = db_session.query(RtvtSessions).filter(
        RtvtSessions.session_code == session_code
    ).first()
    if not _session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Please contact you admin",
        )
    if _session.end_at:
        mes = "Session has already ended"
        logger.debug(mes)
        raise_http_exception(mes)

    _session.end_at = datetime.utcnow()
    db_session.commit()
    