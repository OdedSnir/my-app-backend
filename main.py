from fastapi import FastAPI
from routes.codeblock_r import router as codeblock_router
from sockets.codeblock_ws import router as websocket_router

app = FastAPI()

app.include_router(codeblock_router, prefix="/api/codeblocks")
app.include_router(websocket_router)  # no prefix needed for /ws/{block_id}refix="/api/websockets")