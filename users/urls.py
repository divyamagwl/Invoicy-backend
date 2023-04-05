from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.RegisterAPI.as_view(), name='user-list'),
    path('login/', views.LoginAPI.as_view(), name='user-login'),
    path("fetch-users/", views.UsersListAPI.as_view(), name='fetch-users'),
    path("users/<username>/", views.UsersDetailAPI.as_view(), name='user-detail'),
    path("users/<username>/update-password/", views.UpdatePassword.as_view(), name='user-update-password')
]
