#from users import Users
#user = Users()
class Registration:
  def __init__(self):
    self.users = []

  def get_message(self, username, password,email,phone_number):
    print(username,password,email,phone_number)
    message = "register|" + username + "|" + password + "|" + email + "|" + phone_number
    return message

class LoginName:
  def __init__(self):
    return None
  def get_message(self, username, password):
    print(username, password)
    message = "login_password|" + username + "|" + password
    return message

class LoginEmail:
  def __init__(self):
    return None

  def get_message(self, email, email_code):
    print(email, email_code)
    message = "login_email|" + email + "|" + email_code
    return message

class ForgetPassword:
  def get_message(self, phone_number, phone_code, new_password1, new_password2):
    print(phone_code, phone_number, new_password1, new_password2)
    message = "change_password|" + phone_number + "|" + phone_code + "|" + new_password1 + "|" + new_password2
    return message