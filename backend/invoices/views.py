from rest_framework import generics, permissions

from .models import Invoice
from .serializers import InvoiceCreateSerializer, InvoiceDetailsSerializer, BillDetailsSerializer
from .permissions import IsOwnerOrReadOnly, IsClientOrReadOnly

class InvoiceCreateAPI(generics.CreateAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvoicesListAPI(generics.ListAPIView):
    serializer_class = InvoiceDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)


class InvoiceDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvoiceDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)


class ClientInvoicesListAPI(generics.ListAPIView):
    serializer_class = InvoiceDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        client = self.kwargs.get('client')
        return Invoice.objects.filter(user=self.request.user, client=client)


class BillsListAPI(generics.ListAPIView):
    serializer_class = InvoiceDetailsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(client=self.request.user)


class BillDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BillDetailsSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientOrReadOnly]
    lookup_field = 'id'

    def get_queryset(self):
        return Invoice.objects.filter(client=self.request.user)