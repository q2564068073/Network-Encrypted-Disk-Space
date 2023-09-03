class ForgetPassword:
    def get_message(self,phone_number,phone_code,new_password1,new_password2):
        print(phone_code,phone_number,new_password1,new_password2)
        message = "change_password|" + phone_number + "|" + phone_code+ "|" + new_password1+ "|" + new_password2
        return message