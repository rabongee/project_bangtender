import bcrypt
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from liquor.models import Liquor
from bangtender.base_models import CommonFields


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, name, email, address):
        # 외부 라이브러리를 사용하여 비밀번호를 해시화
        hashed_password = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt())
        user = self.model(
            username=username,
            # 바이트 문자열로 데이터베이스에 저장시 문제가 생길수 있어서 유니코드 문자열로 변환
            password=hashed_password.decode("utf-8"),
            name=name,
            # 이메일의 도메인을 대문자로 받아도 소문자로 데이터베이스에 저장
            email=self.normalize_email(email),
            address=address,
        )
        user.save()
        return user

    def create_superuser(self, username, email, name, password, address=""):
        user = self.create_user(
            username=username,
            password=password,
            name=name,
            email=email,
            address=address,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=20)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(max_length=254, unique=True)
    address = models.CharField(max_length=254)
    date_joined = models.DateTimeField(auto_now_add=True)

    # 고유 식별자로 사용되는 user모델의 필드 이름
    USERNAME_FIELD = "username"
    # 필수로 입력받고 싶은 값으로 createsuperuser시 사용
    REQUIRED_FIELDS = ["name", "email"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    def soft_delete(self):
        self.is_active = False
        self.save()

    # 로그인 해싱 커스터마이징을 위한 check_password 오버라이딩
    def check_password(self, raw_password):
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))


class MyLiquor(CommonFields):
    status_choices = [
        ("1", "내가 보유한 술"),
        ("2", "좋아하는 술"),
        ("3", "싫어하는 술"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="my_user")
    liquor = models.ForeignKey(
        Liquor, on_delete=models.CASCADE, related_name="my_liquor"
    )
    status = models.CharField(max_length=1, choices=status_choices)
