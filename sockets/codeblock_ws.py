from bson import ObjectId
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from database.connection import db
from typing import Dict

router = APIRouter()

rooms: Dict[str, Dict] = {}

@router.websocket("/ws/{block_id}")
async def websocket_endpoint(websocket: WebSocket, block_id: str):
    await websocket.accept()

    # Initialize room if not exists
    if block_id not in rooms:
        defaults: dict = {
            "code": "print('hello world')",
            "solution": "print('Hello World')"
        }

        rooms[block_id] = {
            "mentor": websocket,
            "students": [],
            "code": defaults["code"],
            "solution": defaults["solution"]
        }
        role = "mentor"
        try:
            codeblock = await db.codeblocks.find_one({"_id": ObjectId(block_id)})
            # set code to the initial code of the codeblock
            rooms[block_id]["code"] = codeblock["initial_code"]
            # set solution to the solution for later use
            rooms[block_id]["solution"] = codeblock["solution"]
        except:
            if rooms["code"] == defaults["code"]:
                print("code stayed default for some reason")
            if rooms["solution"] == defaults["solution"]:
                print("solution stayed default for some reason")

    else:
        rooms[block_id]["students"].append(websocket)
        role = "student"

    # Send role and current code to this user
    await websocket.send_json({
        "type": "init",
        "role": role,
        "code": rooms[block_id]["code"],
        "student_count": len(rooms[block_id]["students"]),
        "solution": rooms[block_id]["solution"]
    })

    try:
        while True:
            data = await websocket.receive_text()

            # Only students send updates
            if role == "student":
                rooms[block_id]["code"] = data

                # Broadcast to all students except sender
                for student in rooms[block_id]["students"]:
                    if student != websocket:
                        await student.send_text(data)

                # Also send to mentor
                await rooms[block_id]["mentor"].send_text(data)

    except WebSocketDisconnect:
        if role == "mentor":
            # Kick all students and delete room
            for student in rooms[block_id]["students"]:
                await student.close(code=1000)
            del rooms[block_id]
        else:
            rooms[block_id]["students"].remove(websocket)
