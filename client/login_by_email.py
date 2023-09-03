class LoginEmail:
    def __init__(self):
        return None
    def get_message(self,email,email_code):
        print(email,email_code)
        message = "login_email|" + email + "|" + email_code
        return message