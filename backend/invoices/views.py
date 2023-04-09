from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Invoice
from .serializers import InvoiceCreateSerializer, InvoiceDetailsSerializer
from .permissions import IsOwnerOrReadOnly

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
