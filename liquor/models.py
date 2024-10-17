from django.db import models
from django.conf import settings
from bangtender.base_models import CommonFields


class Liquor(CommonFields):
    """Liquor 모델
    
    Keyword arguments:
    name: Liquor 이름
    classification: Liquor 카테고리
    img: Liquor 이미지
    content: Liquor 내용
    taste: Liquor 맛
    abv: Liquor 도수
    price: Liquor 가격
    bookmark: Liquor 북마크 외래키 참조 필드
    
    """
    
    name = models.CharField(max_length=200)
    classification = models.CharField(max_length=20)
    img = models.ImageField(upload_to="liquor/")  # liquor앱 하위로 이미지 저장
    content = models.TextField()  # 내용(생산지, 특징)
    taste = models.CharField(max_length=500)
    abv = models.DecimalField(max_digits=3, decimal_places=1)
    price = models.PositiveIntegerField()  # 양의 정수만 가능
    bookmark = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="liquor_bookmark")

    def __str__(self):
        return self.name
