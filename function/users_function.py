def response_user(user):
    user_response = {
        "id": user[0],
        "username": user[1],
        "email": user[2],
        "created_at": user[4],
        "is_active": user[5],
    }
    return user_response

def response_users(users: list):
    return [response_user(user) for user in users]

def open_file(filename: str) ->str:
    with open(f"/Users/dimarik/PycharmProjects/TaskManagerApi/TaskManage/{filename}", encoding="utf-8") as f:
        content = f.read()
        return content

