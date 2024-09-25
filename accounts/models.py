import bcrypt
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from liquor.models import Liquor


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, name, email, address):
        # 외부 라이브러리를 사용하여 비밀번호를 해시화
        hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt())
        user = self.model(
            username=username,
            # 바이트 문자열로 데이터베이스에 저장시 문제가 생길수 있어서 유니코드 문자열로 변환
            password=hashed_password.decode('utf-8'),
            name=name,
            # 이메일의 도메인을 대문자로 받아도 소문자로 데이터베이스에 저장
            email=self.normalize_email(email),
            address=address
        )
        user.save()
        return user

    def create_superuser(self, username, email, name, password, address=''):
        user = self.create_user(
            username=username,
            password=password,
            name=name,
            email=email,
            address=address
        )
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=20)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    email = models.EmailField(max_length=254, unique=True)
    address = models.CharField(max_length=254)

    # 고유 식별자로 사용되는 user모델의 필드 이름
    USERNAME_FIELD = 'username'
    # 필수로 입력받고 싶은 값으로 createsuperuser시 사용
    REQUIRED_FIELDS = ['name', 'email']

    objects = CustomUserManager()

    def soft_delete(self):
        self.is_active = False
        self.save()


class BaseLiquorModel(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    class Meta:
        abstract = True


class MyLiquor(BaseLiquorModel):
    liquor = models.ForeignKey(
        Liquor, on_delete=models.CASCADE, related_name='my_liquor')


class LikeLiquor(BaseLiquorModel):
    liquor = models.ForeignKey(
        Liquor, on_delete=models.CASCADE, related_name='like_liquor')


class DislikeLiquor(BaseLiquorModel):
    liquor = models.ForeignKey(
        Liquor, on_delete=models.CASCADE, related_name='dislike_liquor')
