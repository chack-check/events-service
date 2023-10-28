from starlette.websockets import WebSocketState
from fastapi import WebSocket

from .schemas import UserData


class Connection:

    def __init__(self, ws: WebSocket, user_data: UserData):
        self._ws = ws
        self._user_data = user_data

    async def send(self, data: dict) -> None:
        client_ok = self._ws.client_state == WebSocketState.CONNECTED
        app_ok = self._ws.application_state == WebSocketState.CONNECTED
        if client_ok and app_ok:
            print(f"Sending {data} to ws (user_data: {self._user_data})")
            await self._ws.send_json(data)
        else:
            print(f"Client or app is not ok: client - {client_ok}, app - {client_ok}")

    async def read(self) -> None:
        while True:
            await self._ws.receive_json()


class ConnectionsPool:

    def __init__(self):
        self._connections: list[Connection] = []

    async def send(self, users_ids: list[int], data: dict) -> None:
        connections = (c for c in self._connections if c._user_data.id in users_ids)
        for connection in connections:
            await connection.send(data)

    def add_connection(self, connection: Connection):
        self._connections.append(connection)


ws_pool = ConnectionsPool()
