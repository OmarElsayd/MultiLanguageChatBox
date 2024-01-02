from sqlalchemy.orm import Session

from rtvt_services.db_models.models import RtvtUsers, RtvtSessions
from rtvt_services.dependency.exception_handler import TranslationException
from rtvt_services.util.constant import SUPPORTED_LANGS


def verify_session_invitation(user: RtvtUsers, db_session: Session, session_code: str):
    """

    :param user:
    :param db_session:
    :param session_code:
    :return: None if not verified
    """
    # noinspection PyTypeChecker
    verified = db_session.query(
        RtvtSessions.participants,
    ).filter(
        RtvtSessions.session_code == session_code
    ).filter(
        RtvtSessions.participants.contains([user.user_name])
    ).first()

    return verified


def verify_supported_language(target_language_code: str):
    if target_language_code not in SUPPORTED_LANGS:
        raise TranslationException("Unsupported Lang or wrong code")
