USER_CREDENTIALS = {
    "Linda": "pulseritas123",
    "Daira": "pulseritas456"
}

def login_user(username, password):
    return USER_CREDENTIALS.get(username) == password
