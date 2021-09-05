from django.urls import path
from django.urls.conf import include
from friends import views

urlpatterns = [

    ## Testing APi
    path("author_create/", views.AuthorCreateApi.as_view(),name="author_create"),
    path("author_update/<int:pk>/", views.AuthorUpdateApi.as_view(),name="author_update"),
    ## Testing APi

    path("friends/AllPeoples/", views.AllPeoplesApi.as_view(),name="all_peoples"),
    path("friends/user_data/<int:id>/", views.user_data.as_view(),name="user_data"),
]