from django.urls import path
from . import views


urlpatterns = [
    # 칵테일 목록 조회 및 추가 (GET, POST)
    path('', views.CocktailListView.as_view(), name='cocktail_list_create'),

    # 특정 칵테일 상세 조회, 수정 및 삭제 (GET, PUT, DELETE)
    path('<int:pk>/', views.CocktailDetailView.as_view(), name='cocktail_detail'),

    # 특정 칵테일 북마크 (POST)
    # path('<int:pk>/bookmark/', bookmark_cocktail, name='bookmark_cocktail'),

    path("<int:pk>/bookmark/", views.CocktailBookmarkView.as_view(),name="cocktail_bookmark")
]