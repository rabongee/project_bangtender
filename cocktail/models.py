from django.db import models
from django.conf import settings
from bangtender.base_models import CommonFields


class Cocktail(CommonFields):
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
