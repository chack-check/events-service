from grpc.aio import insecure_channel

from .protousers.users_pb2 import UserResponse, GetUserByTokenRequest
from .protousers.users_pb2_grpc import UsersStub
from .project.settings import settings


async def get_user_by_refresh_token(token: str) -> UserResponse:
    async with insecure_channel(settings.users_service_grpc) as channel:
        stub = UsersStub(channel)
        return await stub.GetUserByRefreshToken(GetUserByTokenRequest(token=token))
