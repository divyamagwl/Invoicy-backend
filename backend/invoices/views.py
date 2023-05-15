from rest_framework import generics, status, permissions, views
from rest_framework.response import Response

from .models import Invoice
from .serializers import InvoiceCreateSerializer, InvoiceDetailsSerializer, BillDetailsSerializer, SendReminderSerializer
from .permissions import IsOwnerOrReadOnly, IsClientOrReadOnly

from .email import send_reminder_via_email
from users.models import CustomUser

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
    

class SendReminderAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def post(self, request):
        serializer = SendReminderSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            invoiceid = serializer.data["id"]

            try:
                invoice = Invoice.objects.get(id = invoiceid)
            except:
                return Response({"message": "Something went wrong", "data": "Invalid invoice"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = CustomUser.objects.get(id = invoice.user.id)
            except:
                return Response({"message": "Something went wrong", "data": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                client = CustomUser.objects.get(id = invoice.client.id)
            except:
                return Response({"message": "Something went wrong", "data": "Invalid client"}, status=status.HTTP_400_BAD_REQUEST)

            message = f"""This is a gentle reminder to please pay the bill for the following invoice - \n
            Company name - {user.company_name}\n
            Invoice id - {invoice.id}\n
            Invoice date - {invoice.invoiceDate}\n
            Invoice due date - {invoice.dueDate}\n
            Invoice due amount - {invoice.dueAmount} Rupees\n
            Invoice work completed - {invoice.workCompleted}\n
            """

            send_reminder_via_email(client.email, message)

            return Response({"message": "Reminder sent Successfully", "data": ""}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)