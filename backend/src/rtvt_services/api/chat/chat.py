import logging
from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends, status
from fastapi.websockets import WebSocketState
from sqlalchemy.orm import Session

from rtvt_services.dependency.user_checker import get_curr_user
from rtvt_services.api.util.rtvt_translate import translate_text_
from rtvt_services.api.util.util import (
    verify_session_invitation,
    verify_supported_language,
    update_users_session,
    update_transcript_body_text,
    end_session
)
from rtvt_services.db_engine.session import get_session
from rtvt_services.db_models.models import RtvtUsers
from rtvt_services.dependency.exception_handler import BroadcastException, InvalidInputException
from rtvt_services.util.constant import API_V1_BASE_ROOT, WS_MESSAGE
from rtvt_services.util.payloads import WsMessagePayload, InComingWsMessagePayload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CHAT API")

router = APIRouter(
    prefix=f"{API_V1_BASE_ROOT}/chat_ws",
    tags=["chat_ws"],
    responses={
        404: {"description": "Not found"}
    }
)

connected_clients: dict[str: dict] = {}
"""
    example connected_clients structure:
    {
        session_code+user_id:
            {
                'ws_user': user,
                'ws_connection': websocket,
                'used_language': used_language
            }
    }
"""


class ChatManager:
    @classmethod
    async def connect(
        cls,
        websocket: WebSocket,
        session_code: str,
        user: RtvtUsers,
        db_session: Session,
        used_language: str
    ) -> None:
        """
        Establishes a WebSocket connection for a user to a given session.

        :param websocket: WebSocket connection object.
        :param session_code: Unique code identifying the session.
        :param user: The user object who is connecting.
        :param db_session: Database session for any DB operations.
        :param used_language: Language used by the user.
        """
        user_key = f"{session_code}{user.id}"
        if connected_clients.get(user_key):
            logger.info(f"{user.first_name} {user.last_name} is in the chat already!")
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        verify_session = verify_session_invitation(user, db_session, session_code)
        if not verify_session:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return

        if verify_session.end_at:
            message = {
                "status_code": status.HTTP_423_LOCKED
            }
            await cls._handle_ended_session(websocket, message)
            websocket.client_state = WebSocketState.DISCONNECTED
            return

        await update_users_session(user, verify_session, db_session, used_language)
        await websocket.accept()
        connected_clients[user_key] = {
            'ws_user': user, 'ws_connection': websocket, 'used_language': used_language
        }
        await cls.broadcast_connection_message(
            {
                "status_code": status.HTTP_201_CREATED,
                "user": f"{user.first_name} {user.last_name}",
                "user_name": user.user_name,
                "user_id": str(user.id)
            },
            session_code,
            str(user.id)
        )

    @classmethod
    async def _handle_ended_session(
        cls,
        websocket: WebSocket,
        message: dict,
    ) -> None:
        await websocket.accept()
        await websocket.send_json(message)

    @classmethod
    async def disconnect(cls, session_code: str, user: RtvtUsers, session: Session):
        """

        :param session:
        :param session_code:
        :param user:
        :return:
        """
        if not connected_clients[session_code + str(user.id)]:
            logger.info(f"{user.first_name} {user.last_name}  is not in the chat!")
            return
        logger.info(f"disconnecting session {session_code + str(user.id)}")
        await cls.broadcast_connection_message({
                "status_code": status.HTTP_410_GONE,
                "user": f"{user.first_name} {user.last_name}",
                "user_name": user.user_name,
                "user_id": str(user.id)
            },
            session_code,
            str(user.id)
        )
        del connected_clients[session_code + str(user.id)]
        logger.info(f"disconnected {session_code + str(user.id)} successfully")
        for session_id, _ in connected_clients.items():
            if session_id.startswith(session_code):
                return
        await end_session(session_code=session_code, db_session=session)

    @classmethod
    async def broadcast_connection_message(cls, message: str, session_code: str, user_id: str):
        """

        :param message:
        :param session_code:
        :return:
        """
        try:
            logger.info("Getting evey user in web socket session to send connection message")
            for session_id, session_ws in connected_clients.items():
                if session_id.startswith(session_code) and not session_id.endswith(user_id):
                    logger.info(f"found ws session {session_id}, for session code {session_ws}")
                    await session_ws['ws_connection'].send_json(message)
        except BroadcastException as ws_error:
            logger.error(ws_error)
            raise BroadcastException(ws_error)

    @classmethod
    async def broadcast_chat_message(
            cls, session_code, message_payload: InComingWsMessagePayload
    ):
        try:
            client_ws = connected_clients[session_code + str(message_payload.to_user_id)]["ws_connection"]
            language_model = connected_clients[session_code + str(
                message_payload.to_user_id
            )]["used_language"]
            message_payload = WsMessagePayload(
                type=WS_MESSAGE,
                from_=message_payload.from_,
                to_=message_payload.to_,
                content=message_payload.content,
                lang=language_model
            )
            await client_ws.send_json(message_payload.dict)
        except BroadcastException as ws_error:
            logger.error(ws_error)
            raise BroadcastException(ws_error)

    @classmethod
    def parse_ws_message(cls, raw_message) -> InComingWsMessagePayload:
        if raw_message.get("type") == WS_MESSAGE:
            return InComingWsMessagePayload(**raw_message)
        logger.error("type is not a message")
        raise InvalidInputException("type is not a message")


@router.websocket("/{session_code}/ws/{used_language}/{token}")
async def websocket_endpoint(
        session_code: str,
        used_language: str,
        token: str,
        websocket: WebSocket,
        db_session: Session = Depends(get_session),
):
    from_user = await get_curr_user(token, db_session)
    verify_supported_language(used_language)
    await ChatManager.connect(websocket, session_code, from_user, db_session, used_language)
    try:
        if websocket.client_state == WebSocketState.DISCONNECTED:
            return
        while True:
            raw_json_data = await websocket.receive_json()
            parsed_ws_message = ChatManager.parse_ws_message(raw_json_data)
            if not connected_clients.get(session_code + str(parsed_ws_message.to_user_id)):
                continue
            translated_text = translate_text_(
                source_language_code=parsed_ws_message.source_lang,
                target_language_code=connected_clients[session_code + str(
                    parsed_ws_message.to_user_id
                )]["used_language"],
                text=parsed_ws_message.content
            )

            await update_transcript_body_text(
                db_session, session_code, parsed_ws_message, translated_text, from_user
            )

            parsed_ws_message.content = translated_text
            await ChatManager.broadcast_chat_message(
                session_code=session_code, message_payload=parsed_ws_message
            )
    except WebSocketDisconnect:
        await ChatManager.disconnect(session_code, from_user, db_session)
