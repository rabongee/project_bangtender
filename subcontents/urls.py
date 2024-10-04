from django.urls import path
from . import views

urlpatterns = [
    path("bangtenderbot/", views.BangtenderBot.as_view()),


    # NEWMODULE: 파인튜닝 모델
    # path("fine-tuning/", views.MyFineTuning.as_view()),
]
