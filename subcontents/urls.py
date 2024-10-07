from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainPageAPIView.as_view(), name='mainpage'),
    path('search/', views.SearchAPIView.as_view(), name='search'),
    path('info/', views.InfoAPIView.as_view(), name='info'),
    path("bangtenderbot/", views.BangtenderBot.as_view()),


    # NEWMODULE: 파인튜닝 모델
    # path("fine-tuning/", views.MyFineTuning.as_view()),
]
