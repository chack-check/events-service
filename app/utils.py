from .schemas import UserData


async def get_user_data_by_refresh_token(token: str) -> UserData:
    return UserData(id=1)
