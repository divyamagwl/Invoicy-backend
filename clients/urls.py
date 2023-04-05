from django.urls import path

from . import views

urlpatterns = [
    path("add-client/", views.UserAddClientAPI.as_view(), name='add-client'),
    path("fetch-clients/", views.UserClientsListAPI.as_view(), name='fetch-clients'),
    path("client/<client>/", views.ClientsDetailsAPI.as_view(), name='client-detail'),
]
