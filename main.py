from fastapi import FastAPI
from routes.codeblock_r import router as codeblock_router
from sockets.codeblock_ws import router as websocket_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
#allows frontend to contact the server from same device but different ports.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(codeblock_router, prefix="/api/codeblocks")
app.include_router(websocket_router)  # no prefix needed for /ws/{block_id}refix="/api/websockets")