import datetime
import json

from jose import JWTError, jwt

from app.project.settings import settings

ALGORITHM = "HS256"


def get_token_user_id(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        if not payload['exp'] > datetime.datetime.now(datetime.UTC).timestamp():
            raise ValueError("Incorrect token")

        decoded_sub = json.loads(payload['sub'])
        if "user_id" not in decoded_sub:
            raise ValueError("Incorrect token")

        return decoded_sub['user_id']
    except (KeyError, JWTError):
        raise ValueError("Incorrect token")
