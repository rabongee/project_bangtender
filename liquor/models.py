from django.db import models
from django.conf import settings


class Liquor(models.Model):
    name = models.CharField(max_length=200)
    classification = models.CharField(max_length=20)
    img = models.ImageField(upload_to="liquor/")  # liquor앱 하위로 이미지 저장
    content = models.TextField()  # 내용(생산지, 특징)
    taste = models.CharField(max_length=500)
    abv = models.FloatField()
    price = models.PositiveIntegerField()  # 양의 정수만 가능
    bookmark = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liquor_bookmark")

    def __str__(self):
        return self.name
