from rest_framework import generics, status, permissions
from django.db import IntegrityError
from rest_framework.response import Response

from .models import UserClients
from .serializers import UserClientsSerializer, ClientUpdateSerializer

class UserAddClientAPI(generics.ListCreateAPIView):
    serializer_class = UserClientsSerializer
    queryset = UserClients.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {
                    'message': 'Entry already exists.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        

class UserClientsListAPI(generics.ListAPIView):
    serializer_class = UserClientsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UserClients.objects.filter(user=self.request.user)


class ClientsDetailsAPI(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ClientUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'client'

    def get_queryset(self):
        queryset = UserClients.objects.filter(user=self.request.user)
        lookup_field = self.kwargs.get('client')
        return queryset.filter(client=lookup_field)