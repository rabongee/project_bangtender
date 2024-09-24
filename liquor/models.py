from django.db import models


class Liquor(models.Model):
    name = models.CharField(max_length=50)
    classification = models.CharField(max_length=20)
    img = models.ImageField(upload_to="liquor/")  # liquor앱 하위로 이미지 저장
    content = models.TextField()  # 내용(생산지, 특징)
    taste = models.CharField(max_length=100)
    abv = models.FloatField()
    price = models.PositiveIntegerField()  # 양의 정수만 가능

    def __str__(self):
        return self.name
