
import hashlib
import re

class Registration:
  def __init__(self):
    self.users = []

  #此处组装信息之前对密码复杂度和邮箱以及手机号进行格式检查，如果不符合要求那么会弹出一个框框
  #该部分在前端完成，如果都符合条件则对各个关键字进行消息组装
  def get_message(self, username, password,email,phone_number):

    e = check_email(email)             
    p = check_phone_number(phone_number)
    if e == False or p == False:                        
      return "格式错误"
    else:
      #对密码部分进行md5哈希（32位）
      md=hashlib.md5(password.encode('utf-8'))
      md=md.hexdigest()
      print(username,md,email,phone_number)
      message = "register|" + username + "|" + md + "|" + email + "|" + phone_number
      print(message)
      return message

class LoginName:
  def __init__(self):
    return None
  def get_message(self, username, password):
    md = hashlib.md5(password.encode('utf-8'))
    md=  md.hexdigest()
    print(username, md)
    message = "login_password|" + username + "|" + md
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
    md1= hashlib.md5(new_password1.encode('utf-8'))
    md1=  md1.hexdigest()
    md2= hashlib.md5(new_password2.encode('utf-8'))
    md2=  md2.hexdigest()
    if md1!= md2 :   #此处的返回值改一下
      return False
    print(phone_code, phone_number, md1)
    message = "change_password|" + phone_number + "|" + phone_code + "|" + md1 + "|" + md2
    return message

class GetEmailVerificationCode:
  def get_message(self,email):
    """
    获取邮箱验证码
    :param email:
    :return:
    """
    message = "get_email_code|" + email
    return message
class GetPhoneVerificationCode:
  def get_message(self,phone_number):
    """
    获取手机验证码
    :param phone_number:
    :return:
    """
    message = "get_phone_code|" + phone_number
    return message

#对密码的复杂度进行检查，如果符合复杂度要求，那么返回1；如果不符合返回2
def check_password(password):
  result = re.compile(r'^(?![a-zA-z]+$)(?!\d+$)(?![!@#$%^&*.?]+$)[a-zA-Z\d!@#$%.?^&*]+$')
  if re.fullmatch(result, password):
    k=1
  else:
    k=2
  return k

#检查邮箱格式是否符合要求，如果符合要求返回1，不符合要求返回2
def check_email(email):
      # 邮件格式检查
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    if re.match(pattern, email):
      return True
    else:
      return False

def check_phone_number(phone_number):
    # 手机号码格式检查
    pattern = r'^1\d{10}$'  # 以1开头，后面跟着10位数字
    if re.match(pattern, phone_number):
      return True
    else:
      return False

class GetEmailVerificationCode:
  def get_message(self,email):
    """
    获取邮箱验证码
    :param email:
    :return:
    """
    message = "get_email_code|" + email
    return message
class GetPhoneVerificationCode:
  def get_message(self,phone_number):
    """
    获取手机验证码
    :param phone_number:
    :return:
    """
    message = "get_phone_code|" + phone_number
    return message

class Upload:
  def upload_message(self, username,filename,data,key_hash):
    message = 'upload'+'|'+username+'|'+filename+'|'+data+'|'+key_hash
    return message

  def download_message(self,username,filename,key_hash):
    
    message = 'download'+'|'+username+'|'+filename+'|'+key_hash
    return message

  def get_list_message(self,username):
    message = 'get_list' + '|' + username
    return message
  