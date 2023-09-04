from fastapi import APIRouter, WebSocket

from .utils import get_user_data_by_refresh_token
from .ws_pool import ws_pool, Connection


router = APIRouter()


@router.websocket("/")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    data = await websocket.receive_json()
    assert 'refreshToken' in data
    user_data = await get_user_data_by_refresh_token(data['refreshToken'])
    connection = Connection(websocket, user_data)
    ws_pool.add_connection(connection)
    await connection.read()
