from django.db import models
from bangtender.base_models import CommonFields


class Info(CommonFields):
    """Info 모델
    
    Keyword arguments:
    name: Info 이름
    content: Info 내용
    """
    
    name = models.CharField(max_length=200)
    content = models.TextField()


