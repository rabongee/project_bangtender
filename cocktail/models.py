from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
# Create your models here.


class Cocktail(models.Model):
    name = models.CharField(max_length=200)
    img = models.ImageField(upload_to='cocktails/')
    content = models.TextField()
    ingredients = models.TextField()
    taste = models.CharField(max_length=500)
    abv = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    bookmark = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='cocktail_bookmark')

    def __str__(self):
        return self.name
