import logging

from grpc.aio import insecure_channel

from .project.settings import settings
from .protousers.users_pb2 import (
    GetUserByTokenRequest,  # pyright: ignore[reportAttributeAccessIssue]
)
from .protousers.users_pb2 import (
    UserResponse,  # pyright: ignore[reportAttributeAccessIssue]
)
from .protousers.users_pb2_grpc import UsersStub

logger = logging.getLogger("uvicorn.error")


async def get_user_by_refresh_token(token: str) -> UserResponse:
    logger.debug("Fetching user by refresh token")
    async with insecure_channel(settings.users_service_grpc) as channel:
        stub = UsersStub(channel)
        user = await stub.GetUserByRefreshToken(GetUserByTokenRequest(token=token))
        logger.debug(f"Fetched user by refresh token: {user}")
        return user
