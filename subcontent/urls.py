from django.urls import path
from . import views

urlpatterns = [
    path("/fine-tuning/", views.MyFineTuning.as_view()),
    path("/bangtenderbot/", views.BangtenderBot.as_view()),
]
