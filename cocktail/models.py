from django.db import models
from django.conf import settings
from bangtender.base_models import CommonFields


class Cocktail(CommonFields):
    """Cocktail 모델

    Keyword arguments:
    name: Cocktail 이름
    img: Cocktail 이미지
    content: Cocktail 내용
    ingredients: Cocktail 재료
    taste: Cocktail 맛
    abv: Cocktail 도수
    bookmark: Cocktail 북마크 외래키 참조 필드
    """

    name = models.CharField(max_length=200)
    img = models.ImageField(upload_to='cocktails/')
    content = models.TextField()
    ingredients = models.TextField()
    taste = models.CharField(max_length=500)
    abv = models.DecimalField(max_digits=3, decimal_places=1)
    bookmark = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='cocktail_bookmark', blank=True)

    def __str__(self):
        return self.name
