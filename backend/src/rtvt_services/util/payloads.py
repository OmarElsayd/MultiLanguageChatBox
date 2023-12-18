from dataclasses import dataclass


@dataclass
class InCompingTokenPayload:
    id: int
    user_name: str


@dataclass
class TokenPayload:
    sub: str
    exp: float
