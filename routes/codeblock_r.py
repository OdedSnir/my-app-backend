from fastapi import APIRouter
from database.connection import db
from models.codeblock_m import CodeBlock

router = APIRouter()

@router.get("/")
async def get_all_codeblocks():
    blocks = await db.codeblocks.find().to_list(100)

    for block in blocks:
        block['_id'] = str(block['_id'])
    return blocks