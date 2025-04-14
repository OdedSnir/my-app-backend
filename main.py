from fastapi import FastAPI
from routes.codeblock_r import router as codeblock_router

app = FastAPI()

app.include_router(codeblock_router, prefix="/api/codeblocks")
