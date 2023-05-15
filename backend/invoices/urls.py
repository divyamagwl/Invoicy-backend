from django.urls import path

from . import views

urlpatterns = [
    path("add-invoice/", views.InvoiceCreateAPI.as_view(), name='add-invoice'),
    path("fetch-invoices/", views.InvoicesListAPI.as_view(), name='fetch-invoices'),
    path("invoice/<id>/", views.InvoiceDetailAPI.as_view(), name='invoice-detail'),
    path("client-invoice/<client>/", views.ClientInvoicesListAPI.as_view(), name='client-invoices'),
    path("fetch-bills/", views.BillsListAPI.as_view(), name='my-bills'),
    path("bill/<id>/", views.BillDetailAPI.as_view(), name='bill-detail'),
    path("reminder/invoice/", views.SendReminderAPI.as_view(), name='invoice-reminder'),
]
