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
