import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token                                  

from users.models import CustomUser
from clients.models import UserClients
from clients.models import UserClients

class UserClientsModelTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(
            company_name='John Doe', email="johndoe@gmail.com", username="johndoe", password="test1234"
        )
        self.user2 = CustomUser.objects.create(
            company_name='Jane Doe', email="janedoe@gmail.com", username="janedoe", password="test12345"
        )
        UserClients.objects.create(user=self.user1, client=self.user2, discount=10, blocked=False)

    def test_user_and_client_make_unique_together(self):
        with self.assertRaises(Exception) as context:
            UserClients.objects.create(user=self.user1, client=self.user2, discount=20, blocked=True)
        self.assertIn('Duplicate entry', str(context.exception))

    def test_user_related_name(self):
        user = CustomUser.objects.get(username=self.user1.username)
        user_clients = user.user.all()
        self.assertEqual(user_clients.count(), 1)

    def test_client_related_name(self):
        client = CustomUser.objects.get(username=self.user2.username)
        user_clients = client.client.all()
        self.assertEqual(user_clients.count(), 1)


class UserAddClientAPITest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(
            company_name='John Doe', email="johndoe@gmail.com", username="johndoe", password="test1234"
        )
        self.user2 = CustomUser.objects.create(
            company_name='Jane Doe', email="janedoe@gmail.com", username="janedoe", password="test12345"
        )
        token, _ = Token.objects.get_or_create(user=self.user1)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        self.url = reverse('add-client')
        self.payload = {
            'client': self.user2.id,
            'discount': 10,
            'blocked': False
        }

    def test_create_user_client(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserClients.objects.count(), 1)
        self.assertEqual(UserClients.objects.get().user, self.user1)
        self.assertEqual(UserClients.objects.get().client, self.user2)
        self.assertEqual(UserClients.objects.get().discount, 10)
        self.assertFalse(UserClients.objects.get().blocked)

    def test_create_duplicate_user_client(self):
        UserClients.objects.create(user=self.user1, client=self.user2, discount=10, blocked=True)
        response = self.client.post(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Entry already exists.')

class UserClientsListAPITest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(
            company_name='John Doe', email="johndoe@gmail.com", username="johndoe", password="test1234"
        )
        self.user2 = CustomUser.objects.create(
            company_name='Jane Doe', email="janedoe@gmail.com", username="janedoe", password="test12345"
        )
        self.user3 = CustomUser.objects.create(
            company_name='Jake Doe', email="jakedoe@gmail.com", username="jakedoe", password="test123456"
        )
        self.user1_clients = UserClients.objects.create(user=self.user1, client=self.user2, discount=10, blocked=True)
        self.user1_clients = UserClients.objects.create(user=self.user1, client=self.user3, discount=20, blocked=False)
        token, _ = Token.objects.get_or_create(user=self.user1)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        self.url = reverse('fetch-clients')

    def test_get_user_clients(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['user'], self.user1.id)
        self.assertEqual(response.data[0]['client'], self.user2.id)
        self.assertEqual(response.data[0]['discount'], 10)
        self.assertTrue(response.data[0]['blocked'])
        self.assertEqual(response.data[1]['user'], self.user1.id)
        self.assertEqual(response.data[1]['client'], self.user3.id)
        self.assertEqual(response.data[1]['discount'], 20)
        self.assertFalse(response.data[1]['blocked'])


class ClientsDetailsAPITest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(
            company_name='John Doe', email="johndoe@gmail.com", username="johndoe", password="test1234"
        )
        self.user2 = CustomUser.objects.create(
            company_name='Jane Doe', email="janedoe@gmail.com", username="janedoe", password="test12345"
        )
        self.user3 = CustomUser.objects.create(
            company_name='Jake Doe', email="jakedoe@gmail.com", username="jakedoe", password="test123456"
        )
        self.user1_clients = UserClients.objects.create(user=self.user1, client=self.user2, discount=10, blocked=True)
        self.user1_clients = UserClients.objects.create(user=self.user1, client=self.user3, discount=20, blocked=False)
        token, _ = Token.objects.get_or_create(user=self.user1)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        self.url = reverse('client-detail', args=[self.user2.id])
        self.payload = {
            'discount': 15,
            'blocked': False
        }

    def test_get_client_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user1.id)
        self.assertEqual(response.data['client'], self.user2.id)
        self.assertEqual(response.data['discount'], 10)
        self.assertTrue(response.data['blocked'])

    def test_update_client_details(self):
        response = self.client.put(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(UserClients.objects.get(client=self.user2).discount, 15)
        self.assertFalse(UserClients.objects.get(client=self.user2).blocked)

    def test_delete_client(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserClients.objects.count(), 1)