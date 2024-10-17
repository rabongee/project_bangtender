from django.urls import path
from . import views


urlpatterns = [
    path('', views.CocktailListView.as_view(), name='cocktail_list_create'),
    path('<int:pk>/', views.CocktailDetailView.as_view(), name='cocktail_detail'),
    path("<int:pk>/bookmark/", views.CocktailBookmarkView.as_view(),name="cocktail_bookmark")
]