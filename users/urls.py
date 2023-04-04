from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.UsersAPI.as_view(), name='user-list'),
    path('login/', views.LoginView.as_view(), name='user-login'),
    path("users/<username>/", views.UsersDetailAPI.as_view(), name='user-detail'),
    path("users/<username>/update-password/", views.UpdatePassword.as_view(), name='user-update-password')
]
