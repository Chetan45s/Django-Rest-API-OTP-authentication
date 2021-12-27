from django.urls import path
from accounts import views
from knox.views import LogoutView


urlpatterns = [
    path('sendOtp', views.sendOtp.as_view()),
    path('validateOtp', views.validateOtp.as_view()),
    path('registerUser', views.registerUser.as_view()),
    
    path('login', views.LoginAPI.as_view()),
    path('logout', LogoutView.as_view()),

    path('user_id/', views.UserIDView.as_view(), name='user-id'),
]
  