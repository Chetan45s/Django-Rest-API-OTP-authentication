from django.urls import path
from django.urls.conf import include
from friends import views

urlpatterns = [

    ## Testing APi
    path("author_create/", views.AuthorCreateApi.as_view(),name="author_create"),
    path("author_update/<int:pk>/", views.AuthorUpdateApi.as_view(),name="author_update"),
    ## Testing APi

    path("friends/AllPeoples/", views.AllPeoplesApi.as_view(),name="all_peoples"),
    path("friends/myFriends/", views.showMyFriends.as_view(),name="showMyFriends"),
    path("friends/pendingRequests/", views.pendingRequests.as_view(),name="pendingRequests"),
    path("friends/nonRespondedRequests/", views.nonResponsedRequests.as_view(),name="nonResponsedRequests"),
    path("friends/userData/<int:id>/", views.user_data.as_view(),name="user_data"),
    path("friends/sendRequest/<int:id>/", views.Send_request.as_view(),name="Send_request"),
    path("friends/acceptRequest/<int:id>/", views.Accept_request.as_view(),name="Accept_request"),
    path("friends/deleteRequest/<int:id>/", views.Delete_request.as_view(),name="Delete_request"),
    path("friends/removeFriend/<int:id>/", views.removeFriend.as_view(),name="removeFriend"),
] 