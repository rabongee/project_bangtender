from django.db import models
from bangtender.base_models import CommonFields
# Create your models here.
class Info(CommonFields):
    name = models.CharField(max_length=200)
    content = models.TextField()


