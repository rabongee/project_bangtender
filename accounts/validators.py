import bcrypt
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import User


def validator_signup(signup_data):
    err_msg = []

    if (username := signup_data.get("username")):
        if User.objects.filter(username=username).exists():
            err_msg.append({"username": "이미 존재하는 아이디입니다."})
    else:
        err_msg.append({"username": "아이디를 입력하지 않았습니다."})

    password = signup_data.get("password")
    password_confirm = signup_data.get("password_confirm")
    if not password or not password_confirm:
        err_msg.append({"password": "비밀번호와 비밀번호 확인칸을 모두 입력해야 합니다."})
    elif not password == password_confirm:
        err_msg.append({"password": "비밀번호가 일치하지 않습니다."})
    else:
        try:
            validate_password(password)
        except ValidationError:
            err_msg.append({"password": "비밀번호가 형식에 맞지 않습니다."})

    if (name := signup_data.get("name")):
        if len(name) > 20:
            err_msg.append({"name": "이름은 20자 이하여야 합니다."})
    else:
        err_msg.append({"name": "이름을 입력하지 않았습니다."})

    if (email := signup_data.get("email")):
        if User.objects.filter(email=email).exists():
            err_msg.append({"email": "이미 존재하는 이메일입니다."})
        else:
            try:
                validate_email(email)
            except:
                err_msg.append({"email": "이메일 형식이 올바르지 않습니다."})
    else:
        err_msg.append({"email": "이메일을 입력하지 않았습니다."})

    if not (address := signup_data.get("address")):
        err_msg.append({"address": "주소를 입력하지 않았습니다."})

    return not bool(err_msg), err_msg


def validator_update_user(update_data, user_data):
    err_msg = []

    name = update_data.get("name", user_data.name)
    if name =="":
        err_msg.append({"name": "이름을 입력해야 합니다."})
    elif len(name) > 20:
        err_msg.append({"name": "이름은 20자 이하여야 합니다."})

    email = update_data.get("email", user_data.email)  
    if email == "": 
        err_msg.append({"email": "이메일을 입력해야 합니다."})
    elif User.objects.filter(email=email).exclude(pk=user_data.pk).exists(): 
        err_msg.append({"email": "이미 존재하는 이메일입니다."})
    else: 
        try: 
            validate_email(email)
        except: 
         err_msg.append({"email": "이메일 형식이 올바르지 않습니다."})


    address = update_data.get("address", user_data.address)
    if address == "":
        err_msg.append({"address": "주소를 입력해야 합니다."})

    return not bool(err_msg), err_msg


def validator_change_password(password_data, user):
    old_password = password_data.get("old_password")
    new_password = password_data.get("new_password")

    if not old_password or not new_password:
        return False, "기존 패스워드와 새 패스워드를 모두 입력해야 합니다."

    if not bcrypt.checkpw(old_password.encode('utf-8'), user.password.encode('utf-8')):
        return False, "기존 패스워드가 올바르지 않습니다."

    if old_password == new_password:
        return False, "새 패스워드는 기존 패스워드와 달라야 합니다."

    try:
        validate_password(new_password, user=user)
    except ValidationError:
        return False, "새 패스워드가 형식에 맞지 않습니다."

    return True, None