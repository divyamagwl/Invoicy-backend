import json 
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token                                  

from .models import CustomUser
from .serializers import UsersSerializer, UserUpdateSerializer

# initialize the APIClient app
client = Client()

class CustomUserTest(TestCase):
    """ Test module for CustomUser model """

    def setUp(self):
        CustomUser.objects.create(
            company_name='John Doe', email="johndoe@gmail.com", username="johndoe", password="test1234"
        )
        CustomUser.objects.create(
            company_name='Jane Doe', email="janedoe@gmail.com", username="janedoe", password="test12345"
        )

    def test_user_emails(self):
        user_john = CustomUser.objects.get(username='johndoe')
        user_jane = CustomUser.objects.get(username='janedoe')

        self.assertEqual(user_john.email, "johndoe@gmail.com")
        self.assertEqual(user_jane.email, "janedoe@gmail.com")


class FetchAllUserTest(TestCase):
    """ Test module for GET all User API """

    def setUp(self):
        CustomUser.objects.create(
            company_name='John Doe', email="johndoe@gmail.com", username="johndoe", password="test1234"
        )
        CustomUser.objects.create(
            company_name='Jane Doe', email="janedoe@gmail.com", username="janedoe", password="test12345"
        )

    def test_get_all_users(self):
        # get API response
        response = client.get(reverse('fetch-users'))
        # get data from db
        users = CustomUser.objects.all()
        serializer = UsersSerializer(users, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class FetchUserDetail(TestCase):
    """ Test module for GET fetch user detail API """

    def setUp(self):
        self.john = CustomUser.objects.create(
            company_name='John Doe', email="johndoe@gmail.com", username="johndoe", password="test1234"
        )
        self.jane = CustomUser.objects.create(
            company_name='Jane Doe', email="janedoe@gmail.com", username="janedoe", password="test12345"
        )
        token, _ = Token.objects.get_or_create(user=self.john)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)


    def test_get_valid_user_by_username(self):
        response = self.client.get(
            reverse('user-detail', kwargs={'username': self.john.username}))
        user_john = CustomUser.objects.get(username=self.john.username)
        serializer = UserUpdateSerializer(user_john)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_user_by_username(self):
        response = self.client.get(
            reverse('user-detail', kwargs={'username': "invalid"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RegisterNewUserTest(TestCase):
    """ Test module for registering a new user """

    def setUp(self):
        self.valid_payload = {
            "company_name": 'John Doe', 
            "email": "johndoe@gmail.com", 
            "username": "johndoe", 
            "password": "test1234"
        }
        self.invalid_payload = {
            "company_name": 'John Doe', 
            "email": "johndoe@gmail.com", 
            "username": "johndoe", 
            "password": ""
        }

    def test_register_valid_user(self):
        response = client.post(
            reverse('user-list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_invalid_user(self):
        response = client.post(
            reverse('user-list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginUserTest(TestCase):
    """ Test module for login an existing user record """

    def setUp(self):
        self.register_payload = {
            "company_name": 'John Doe', 
            "email": "johndoe@gmail.com", 
            "username": "johndoe", 
            "password": "test1234"
        }

        client.post(
            reverse('user-list'),
            data=json.dumps(self.register_payload),
            content_type='application/json'
        )

        self.valid_payload = {
            "username": self.register_payload["username"],
            "password": self.register_payload["password"] 
        }
        self.invalid_payload = {
            "username": self.register_payload["username"],
            "password": "invalid" 
        }
        


    def test_valid_login_user(self):
        response = client.post(
            reverse('user-login'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_invalid_update_puppy(self):
        response = client.post(
            reverse('user-login'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateUserTest(TestCase):
    """ Test module for updating an existing user record """

    def setUp(self):
        self.john = CustomUser.objects.create(
            company_name='John Doe', email="johndoe@gmail.com", username="johndoe", password="test1234"
        )
        self.jane = CustomUser.objects.create(
            company_name='Jane Doe', email="janedoe@gmail.com", username="janedoe", password="test12345"
        )
        self.valid_payload = {
            "company_name": 'John Doe Great', 
        }
        self.invalid_payload = {
            "not_company_name": 'John Doe', 
        }
        token, _ = Token.objects.get_or_create(user=self.john)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_valid_update_user(self):
        response = self.client.put(
            reverse('user-detail', kwargs={'username': self.john.username}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_puppy(self):
        response = self.client.put(
            reverse('user-detail', kwargs={'username': self.john.username}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class DeleteUserTest(TestCase):
    """ Test module for deleting an existing user record """

    def setUp(self):
        self.john = CustomUser.objects.create(
            company_name='John Doe', email="johndoe@gmail.com", username="johndoe", password="test1234"
        )
        self.jane = CustomUser.objects.create(
            company_name='Jane Doe', email="janedoe@gmail.com", username="janedoe", password="test12345"
        )
        token, _ = Token.objects.get_or_create(user=self.john)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_valid_delete_user(self):
        response = self.client.delete(
            reverse('user-detail', kwargs={'username': self.john.username}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_user(self):
        response = self.client.delete(
            reverse('user-detail', kwargs={'username': "invalid"}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)