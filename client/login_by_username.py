class LoginName:
    def __init__(self):
        return None
    def get_message(self,username,password):
        print(username,password)
        message = "login_password|" + username + "|" + password
        return message