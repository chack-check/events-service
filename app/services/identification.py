import datetime
import json
import logging

from jose import JWTError, jwt

from app.project.settings import settings

ALGORITHM = "HS256"

logger = logging.getLogger("uvicorn.error")


def get_token_user_id(token: str) -> int:
    logger.debug(f"Fetching user id from token: {token}")
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        logger.debug(f"Token payload: {payload}")
        if not payload['exp'] > datetime.datetime.now(datetime.UTC).timestamp():
            logger.warning(f"Token expired: {payload['exp']}")
            raise ValueError("Incorrect token")

        decoded_sub = json.loads(payload['sub'])
        logger.debug(f"Decoded token sub: {decoded_sub}")
        if "user_id" not in decoded_sub:
            logger.warning("There is no user id in token sub")
            raise ValueError("Incorrect token")

        return decoded_sub['user_id']
    except (KeyError, JWTError) as e:
        logger.exception(e)
        raise ValueError("Incorrect token")
