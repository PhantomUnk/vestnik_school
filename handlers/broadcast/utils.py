import os
import json

USERS_FILE_PATH = os.path.join("files", "users.json")

def add_user(user_id: int):
    users = get_broadcast_users()

    if user_id not in users:
        users.append(user_id)
        status = True
    else:
        users.remove(user_id)
        status = False
    
    with open(USERS_FILE_PATH, "w+", encoding="utf-8") as file:
            json.dump(users, file, ensure_ascii=False)

    return status


def get_broadcast_users() -> list[int]:
    if not os.path.exists(USERS_FILE_PATH):
        return []
    with open(USERS_FILE_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []