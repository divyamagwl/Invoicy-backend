from rest_framework import generics, status, permissions, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from users.models import CustomUser
from users.serializers import UsersSerializer, UserRegistrationSerializer, UserLoginSerializer, UserUpdateSerializer, UpdatePasswordSerializer, VerificationSerializer
from users.permissions import IsOwnerOrReadOnly

from django.contrib.auth import login
from rest_framework.authentication import TokenAuthentication

from .email import send_otp_via_email

class UsersListAPI(generics.ListCreateAPIView):
    serializer_class = UsersSerializer
    queryset = CustomUser.objects.all()


class RegisterAPI(generics.ListCreateAPIView):
    """
    This view provides 'list' for all users and 'create' new users.
    """
    serializer_class = UserRegistrationSerializer
    queryset = CustomUser.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                details = serializer.data
                send_otp_via_email(details["email"])
                details['token'] = token.key
                return Response(details, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):        
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            if user:
                login(request, user)
                token, _ = Token.objects.get_or_create(user=user)
                data = {
                    'user_id': user.id,
                    'username': user.username,
                    'company_name': user.company_name,
                    'token': token.key,
                    'message': 'Logged in successfully'
                }
                return Response(data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)     


class UsersDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    This view provides 'retrieve', 'update', 'destroy' actions to appropriate users.
    """
    serializer_class = UserUpdateSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'username'

class UsersDetailByIDAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    This view provides 'retrieve', 'update', 'destroy' actions to appropriate users.
    """
    serializer_class = UserUpdateSerializer
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'

class UpdatePassword(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = UpdatePasswordSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    lookup_field = 'username'

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = UpdatePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            current_password = serializer.data.get("current_password")
            if not self.object.check_password(current_password):
                return Response({"current_password": ["Wrong password."]}, 
                                status=status.HTTP_400_BAD_REQUEST)

            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutAPI(views.APIView):
    def get(self, request, format=None):
        request.session.flush() # Removes Session from Storage
        try:
            request.user.auth_token.delete() # Deletes Token for current logged in user
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class VerifyOTPAPI(generics.CreateAPIView):
    serializer_class = VerificationSerializer

    def post(self, request):
        serializer = VerificationSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data["email"]
            otp = serializer.data["otp"]

            user = CustomUser.objects.filter(email = email)

            if not user.exists():
                return Response({"message": "Something went wrong", "data": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)
            
            user = user.first()
            if user.otp != otp:
                return Response({"message": "Something went wrong", "data": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)

            user.is_verified = True
            user.save()
            return Response({"message": "Account Verified Successfully", "data": ""}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)