from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    path("",  views.LiquorListView.as_view(), name="liquor_list"),
    path("<int:pk>/",  views.LiquorDetailView.as_view(), name="liquor_detail"),
    path("<int:pk>/bookmark/",  views.LiquorBookmarkView.as_view(),
         name='liquor_bookmark'),
]
=======
    path("", views.LiquorListView.as_view(), name="liquor_list"),
    path("<int:pk>/", views.LiquorDetailView.as_view(), name="liquor_detail"),
    path("<int:pk>/bookmark/", views.LiquorBookmarkView.as_view(), name="liquor_bookmark"),
]
>>>>>>> dev
