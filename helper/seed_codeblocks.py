import sys
import os
import asyncio

# Add backend/ to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.connection import get_DB_connection


db = get_DB_connection()

seed_data = [
    {
        "title": "Async Case",
        "initial_code": "async function fetchData() {\n  const res = await fetch('/api');\n}",
        "solution": "async function fetchData() {\n  const res = await fetch('/api');\n  const data = await res.json();\n  return data;\n}"
    },
    {
        "title": "Array Map",
        "initial_code": "const result = [1, 2, 3].map(x => x);",
        "solution": "const result = [1, 2, 3].map(x => x * 2);"
    },
    {
        "title": "Promise Chain",
        "initial_code": "fetch('/api').then(res => console.log(res));",
        "solution": "fetch('/api')\n  .then(res => res.json())\n  .then(data => console.log(data));"
    },
    {
        "title": "Function Hoisting",
        "initial_code": "console.log(sayHi);\nfunction sayHi() { return 'hi'; }",
        "solution": "function sayHi() { return 'hi'; }\nconsole.log(sayHi());"
    }
]

async def seed():
    await db.codeblocks.delete_many({})  # clear old entries (optional)
    result = await db.codeblocks.insert_many(seed_data)
    print(f"Inserted {len(result.inserted_ids)} code blocks.")

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(seed())
