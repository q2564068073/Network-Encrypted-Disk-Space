#from users import Users
#user = Users()
class Registration:
  def __init__(self):
    self.users = []

  def get_message(self, username, password,email,phone_number):
    print(username,password,email,phone_number)
    message = "register|" + username + "|" + password + "|" + email + "|" + phone_number
    return message
