from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import CustomUser

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'company_name', 'username', 'email', 'is_verified')


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'company_name', 'username',
                  'email', 'password')
        write_only_fields = ('password',)

    #To store password in hash format we need to overwrite create and update functions
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super(UserRegistrationSerializer, self).update(instance, validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                msg = 'Access denied: Wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')

        return user

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'company_name', 'username',
                  'email', 'password')
        read_only_fields = ('username', 'email', 'password')


class UpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'otp')
