from django.urls import path
from .views import LiquorListView, LiquorDetailView
urlpatterns = [
    path('liquors/', LiquorListView.as_view(), name='liquor_list'),
    path('liquors/<int:id>/', LiquorDetailView.as_view(), name='liquor_detail'),
]
