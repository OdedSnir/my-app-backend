import asyncio

from bson import ObjectId
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from database.connection import db
from typing import Dict
from helper.helper import codes_match

router = APIRouter()

rooms: Dict[str, Dict] = {}

@router.websocket("/ws/{block_id}")
async def websocket_endpoint(websocket: WebSocket, block_id: str):
    await websocket.accept()

    role = "student"  # default fallback role
    defaults: dict = {
        "code": "print('hello world')",
        "solution": "print('Hello World')"
    }

    # Initialize room if not exists
    if block_id not in rooms:
        rooms[block_id] = {
            "mentor": websocket,
            "students": [],
            "code": defaults["code"],
            "solution": defaults["solution"],
            "solved": False
        }
        role = "mentor"
        try:
            codeblock = await db.codeblocks.find_one({"_id": ObjectId(block_id)})
            rooms[block_id]["code"] = codeblock["initial_code"]
            rooms[block_id]["solution"] = codeblock["solution"]
        except:
            if rooms[block_id]["code"] == defaults["code"]:
                print("code stayed default for some reason")
            if rooms[block_id]["solution"] == defaults["solution"]:
                print("solution stayed default for some reason")
    else:
        rooms[block_id]["students"].append(websocket)

    # ✅ Send initial message to *everyone*
    await websocket.send_json({
        "type": "init",
        "role": role,
        "code": rooms[block_id]["code"],
        "student_count": len(rooms[block_id]["students"]),
        "solution": rooms[block_id]["solution"],
        "solved": rooms[block_id]["solved"]
    })

    # ✅ Optional: immediate update after init
    await websocket.send_json({
        "type": "update",
        "role": role,
        "code": rooms[block_id]["code"],
        "student_count": len(rooms[block_id]["students"]),
        "solved": rooms[block_id]["solved"]
    })

    try:
        while True:
            data = await websocket.receive_json()
            print(data)

            if role == "student":
                rooms[block_id]["code"] = data['code']
                print(f"checking if {rooms[block_id]['code']} is the same as {rooms[block_id]['solution']}")
                rooms[block_id]["solved"] = codes_match(
                    rooms[block_id]["code"], rooms[block_id]["solution"]
                )
                if rooms[block_id]["solved"]:
                    print(f"websocket {websocket} solved the problem")
                    for student in rooms[block_id]["students"]:
                        await student.send_json({
                            "type": "finished",
                            "message": "Code successfully solved!"
                        })
                    await rooms[block_id]["mentor"].send_json({
                        "type": "finished",
                        "message": "Code successfully solved!"
                    })

                # Broadcast update to all students
                for student in rooms[block_id]["students"]:
                    await student.send_json({
                        "type": "update",
                        "code": data['code'],
                        "solved": rooms[block_id]["solved"]
                    })

                # Also notify the mentor
                await rooms[block_id]["mentor"].send_json({
                    "type": "update",
                    "code": data['code'],
                    "solved": rooms[block_id]["solved"]
                })

    except WebSocketDisconnect:
        if role == "mentor":
            for student in rooms[block_id]["students"]:
                try:
                    student.send_json({
                        "type": "update",
                        "message": "Mentor left. Closing room.",
                    })
                    await student.close(code=1000)
                except RuntimeError:
                    print(f"⚠️ Could not notify student in {block_id}, socket may already be closed.")


            del rooms[block_id]
            print(f"now rooms looks like this:\n{rooms}\n")
        else:
            if block_id in rooms and websocket in rooms[block_id]["students"]:
                rooms[block_id]["students"].remove(websocket)


@router.websocket("/ws/rooms/")
async def rooms_data_endpoint(websocket: WebSocket):
    await websocket.accept()
    print("📡 Monitor connected to /ws/rooms/")

    try:
        while True:
            current_rooms_copy = rooms.copy()
            data = {}

            for block_id, info in current_rooms_copy.items():
                data[block_id] = {
                    "student_count": len(info.get("students", [])),
                    "mentor": str(info.get("mentor").client) if "mentor" in info else "none",
                    "code": info.get("code", ""),
                    "solved": info.get("solved", False)
                }

            await websocket.send_json(data)
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        print("📴 Monitor WebSocket disconnected from /ws/rooms/")
