import json
import logging
from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
from sqlalchemy.orm import Session

from rtvt_services.api.util.util import verify_session_invitation, verify_supported_language
from rtvt_services.db_engine.session import get_session
from rtvt_services.db_models.models import RtvtUsers
from rtvt_services.dependency.exception_handler import BroadcastException, InvalidInputException
from rtvt_services.dependency.role_checker import user_pass
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


class ChatManager:
    @classmethod
    async def connect(
            cls, websocket: WebSocket, session_code: str, user: RtvtUsers, db_session: Session, used_language: str
    ):
        """

        :param used_language:
        :param websocket:
        :param session_code:
        :param user:
        :param db_session:
        :return:
        """
        if connected_clients[session_code + str(user.id)]:
            logger.info(f"{user.first_name} {user.last_name} is in the chat already!")
            return
        if not verify_session_invitation(user, db_session, session_code):
            return
        await websocket.accept()
        connected_clients[session_code + str(user.id)] = {
            'ws_user': user, 'ws_connection': websocket, 'used_language': used_language
        }
        await cls.broadcast_connection_message(
            f"{user.first_name} {user.last_name} has joined the chat",
            session_code,
        )

    @classmethod
    async def disconnect(cls, session_code: str, user: RtvtUsers):
        """

        :param session_code:
        :param user:
        :return:
        """
        if not connected_clients[session_code + str(user.id)]:
            logger.info(f"{user.first_name} {user.last_name}  is not in the chat!")
            return
        logger.info(f"disconnecting session {session_code + str(user.id)}")
        await cls.broadcast_connection_message(
            f"{user.first_name} {user.last_name}  has left the chat",
            session_code,
        )
        del connected_clients[session_code + str(user.id)]
        logger.info(f"disconnected {session_code + str(user.id)} successfully")

    @classmethod
    async def broadcast_connection_message(cls, message: str, session_code: str):
        """

        :param message:
        :param session_code:
        :return:
        """
        try:
            logger.info("Getting evey user in web socket session to send connection message")
            for session_id, session_ws in connected_clients.items():
                if session_id.startwith(session_code):
                    logger.info(f"found ws session {session_id}, for session code {session_ws}")
                    await session_ws.send_text(message)
        except BroadcastException as ws_error:
            logger.error(ws_error)
            raise BroadcastException(ws_error)

    @classmethod
    async def broadcast_chat_message(
            cls, from_user: RtvtUsers, session_code, message_payload: InComingWsMessagePayload
    ):
        try:
            client_ws = connected_clients[session_code + str(message_payload.to_user_id)]["ws_connection"]
            to_user_model = connected_clients[session_code + str(message_payload.to_user_id)]["ws_user"]
            message_payload = WsMessagePayload(
                type=WS_MESSAGE,
                from_="{first_name} {last_name}".format(
                    first_name=from_user.first_name, last_name=from_user.last_name
                ),
                to_="{first_name} {last_name}".format(
                    first_name=to_user_model.first_name, last_name=to_user_model.last_name
                ),
                content=message_payload.content
            )
            await client_ws.send_text(message_payload.dict)
        except BroadcastException as ws_error:
            logger.error(ws_error)
            raise BroadcastException(ws_error)

    @classmethod
    def parse_ws_message(cls, raw_message) -> InComingWsMessagePayload:
        message_data = json.loads(raw_message)

        if message_data.get("type") == WS_MESSAGE:
            return InComingWsMessagePayload(**message_data)
        logger.error("type is not a message")
        raise InvalidInputException("type is not a message")


@router.websocket("/{session_code}/ws")
async def websocket_endpoint(
        session_code: str,
        used_language: str,
        websocket: WebSocket,
        from_user: RtvtUsers = Depends(user_pass),
        db_session: Session = Depends(get_session),
):
    verify_supported_language(used_language)
    await ChatManager.connect(websocket, session_code, from_user, db_session, used_language)
    try:
        while True:
            data = await websocket.receive_text()
            parsed_ws_message = ChatManager.parse_ws_message(data)
            # process ws message and translate if needed
            await ChatManager.broadcast_chat_message(
                from_user=from_user, session_code=session_code, message_payload=parsed_ws_message
            )
    except WebSocketDisconnect:
        await ChatManager.disconnect(session_code, from_user)



