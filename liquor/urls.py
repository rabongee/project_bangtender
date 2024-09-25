from django.urls import path
from .views import LiquorListView, LiquorDetailView

urlpatterns = [
    path("", LiquorListView.as_view(), name="liquor_list"),
    path("v1/liquor/<int:pk>/", LiquorDetailView.as_view(), name="liquor_detail"),
]
