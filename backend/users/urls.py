from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterAPI.as_view(), name='user-list'),
    path('login/', views.LoginAPI.as_view(), name='user-login'),
    path('logout/', views.LogoutAPI.as_view(), name='user-logout'),
    path("fetch-users/", views.UsersListAPI.as_view(), name='fetch-users'),
    path("users/<username>/", views.UsersDetailAPI.as_view(), name='user-detail'),
    path("users/id/<id>/", views.UsersDetailByIDAPI.as_view(), name='user-detail-by-id'),
    path("users/<username>/update-password/", views.UpdatePassword.as_view(), name='user-update-password'),
    path('verify/', views.VerifyOTPAPI.as_view(), name='user-verify'),
]
