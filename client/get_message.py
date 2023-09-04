
import hashlib
import re

class Registration:
  def __init__(self):
    self.users = []

  #此处组装信息之前对密码复杂度和邮箱以及手机号进行格式检查，如果不符合要求那么会弹出一个框框
  #该部分在前端完成，如果都符合条件则对各个关键字进行消息组装
  def get_message(self, username, password,email,phone_number):
    '''
    k=check_password(password)
    if k == 2:   #2代表不符合要求
      return 1
    e=checkemail(email)             #此处注释默认已经完成检查，准许消息的组装
    if e==2:                        #False返回值需要被修改，encode方法不支持bool类型
      return 2
    p=chec_phone_number(phone_number)
    if p==2:
      return 3
    '''
    #对密码部分进行md5哈希（32位）
    md=hashlib.md5(password.encode('utf-8'))
    md=md.hexdigest()
    print(username,md,email,phone_number)
    message = "register|" + username + "|" + md + "|" + email + "|" + phone_number
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
def checkemail(address):
  """
  利用正则表达式检测邮箱格式
  """
  regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
  if re.fullmatch(regex, address):
    t = 1
  else:
    t = 2
  return t

def chec_phone_number(phone_number):
  result = re.compile(r'^(13[0-9]|14[5|7]|15[0|1|2|3|5|6|7|8|9]|18[0|1|2|3|5|6|7|8|9])\d{8}$')
  if re.fullmatch(result, phone_number):
    k=1
  else:
    k=2
  return k

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
  def upload_message(self, username,filename,data,key_hash,data_hash,path):
    with open(path, 'r') as file:
        # 读取文件内容并存储到变量中
        message = 'upload'+'|'+username+'|'+filename+'|'+data+'|'+key_hash+'|'+data_hash+'|'+file.read()
    return message

  def download_message(self,username,filename,key_hash):
    
    message = 'download'+'|'+username+'|'+filename+'|'+key_hash
    return message
  