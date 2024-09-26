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
        if len(name)>20:
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
