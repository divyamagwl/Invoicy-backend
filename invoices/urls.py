from django.urls import path

from . import views

urlpatterns = [
    path("add-invoice/", views.InvoiceCreateAPI.as_view(), name='add-invoice'),
    path("fetch-invoices/", views.InvoicesListAPI.as_view(), name='fetch-invoices'),
    path("invoice/<id>/", views.InvoiceDetailAPI.as_view(), name='invoice-detail'),
]
