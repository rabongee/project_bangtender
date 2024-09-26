from django.urls import path
from . import views

urlpatterns = [
    path("",  views.LiquorListView.as_view(), name="liquor_list"),
    path("v1/liquor/<int:pk>/",  views.LiquorDetailView.as_view(), name="liquor_detail"),
    path("v1/liquor/<int:pk>/bookmark/",  views.LiquorBookmarkView.as_view(), name='liquor_bookmark'),
]
