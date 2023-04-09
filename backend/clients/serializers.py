from rest_framework import serializers

from .models import UserClients

class UserClientsSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = UserClients
        fields = "__all__"

class ClientUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClients
        fields = "__all__"
        read_only_fields = ('user', 'client')
