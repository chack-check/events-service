import msgspec
from fastapi import APIRouter, WebSocket

from .grpc_client import get_user_by_refresh_token
from .ws_pool import ws_pool, Connection


router = APIRouter()


@router.websocket("/")
async def ws_endpoint(websocket: WebSocket):
    try:
        await websocket.accept()
        data = await websocket.receive()
        json_data = msgspec.json.decode(data['text'])
        assert json_data.get('refreshToken'), json_data
        user_data = await get_user_by_refresh_token(json_data['refreshToken'])
        connection = Connection(websocket, user_data)
        ws_pool.add_connection(connection)
        while True:
            await connection.read()
    except Exception:
        await websocket.close()
        raise
