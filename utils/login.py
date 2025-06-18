USER_CREDENTIALS = {
    "linda": "pulseritas123",
    "daira": "braceletgirl"
}

def login_user(username, password):
    return USER_CREDENTIALS.get(username) == password
