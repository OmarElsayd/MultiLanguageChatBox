from dataclasses import dataclass
from pydantic import BaseModel


@dataclass
class InCompingTokenPayload:
    id: int
    user_name: str


@dataclass
class TokenPayload:
    sub: str
    exp: float


@dataclass
class WsMessagePayload:
    type: str
    from_: str
    to_: str
    content: str
    lang: str

    @property
    def dict(self):
        return vars(self)


@dataclass
class InComingWsMessagePayload:
    type: str
    from_: str
    to_: str
    to_user_id: int
    content: str
    source_lang: str
    created_at: str

    @property
    def dict(self):
        return vars(self)


class UserInput(BaseModel):
    user_name: str
    email: str
    password: str
    first_name: str
    last_name: str


class SignupOutput(BaseModel):
    status_code: int


class TokenResponse(BaseModel):
    status_code: int
    access_token: str
    token_type: str = "bearer"


class SessionPayload(BaseModel):
    """
    invitee: user_name
    """
    invitee: str
    passcode: str = None
    is_call: bool = False
