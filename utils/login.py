USER_CREDENTIALS = {
    "Linda": "pulseritas123",
    "Daira": "pulseritas456",
    "Stanford": "codeinplace"
}

def login_user(username, password):
    return USER_CREDENTIALS.get(username) == password
