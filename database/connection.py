from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient

def get_DB_connection() -> AsyncIOMotorClient:
    load_dotenv()
    MONGO_URI = os.getenv("MONGO_URI")

    client = AsyncIOMotorClient(MONGO_URI)
    db = client["codeblocks_db"]
    return db


db = get_DB_connection()