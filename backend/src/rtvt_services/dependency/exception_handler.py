from fastapi import HTTPException, status


class TranslationException(Exception):
    pass


class SshDbEngineException(Exception):
    pass


class BroadcastException(Exception):
    pass


class InvalidInputException(Exception):
    pass


def raise_http_exception(error):
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=str(error)
    )
