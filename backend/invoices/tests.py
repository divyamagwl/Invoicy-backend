import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token                                  

from users.models import CustomUser
from invoices.models import Invoice, Item

class InvoiceModelTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(
            company_name='John Doe', email="johndoe@gmail.com", username="johndoe", password="test1234"
        )
        self.user2 = CustomUser.objects.create(
            company_name='Jane Doe', email="janedoe@gmail.com", username="janedoe", password="test12345"
        )
        self.newInvoice = Invoice.objects.create(user=self.user1, client=self.user2, invoiceDate='2023-05-13', dueDate='2023-05-20', totalAmount=100.00, dueAmount=50.00, advancePercent=50, workCompleted=False, note='Test note')

    def test_user_is_not_null(self):
        invoice = Invoice.objects.get(id=self.newInvoice.id)
        field_null = invoice._meta.get_field('user').null
        self.assertEqual(field_null, False)

    def test_client_is_not_null(self):
        invoice = Invoice.objects.get(id=self.newInvoice.id)
        field_null = invoice._meta.get_field('client').null
        self.assertEqual(field_null, False)

    def test_invoice_date_is_not_null(self):
        invoice = Invoice.objects.get(id=self.newInvoice.id)
        field_null = invoice._meta.get_field('invoiceDate').null
        self.assertEqual(field_null, False)

    def test_due_date_is_not_null(self):
        invoice = Invoice.objects.get(id=self.newInvoice.id)
        field_null = invoice._meta.get_field('dueDate').null
        self.assertEqual(field_null, False)

    def test_total_amount_is_not_null(self):
        invoice = Invoice.objects.get(id=self.newInvoice.id)
        field_null = invoice._meta.get_field('totalAmount').null
        self.assertEqual(field_null, False)

    def test_due_amount_is_not_null(self):
        invoice = Invoice.objects.get(id=self.newInvoice.id)
        field_null = invoice._meta.get_field('dueAmount').null
        self.assertEqual(field_null, False)

    def test_advance_percent_is_not_null(self):
        invoice = Invoice.objects.get(id=self.newInvoice.id)
        field_null = invoice._meta.get_field('advancePercent').null
        self.assertEqual(field_null, False)

    def test_work_completed_is_not_null(self):
        invoice = Invoice.objects.get(id=self.newInvoice.id)
        field_null = invoice._meta.get_field('workCompleted').null
        self.assertEqual(field_null, False)

    def test_note_is_not_null(self):
        invoice = Invoice.objects.get(id=self.newInvoice.id)
        field_null = invoice._meta.get_field('note').null
        self.assertEqual(field_null, False)

    def test_invoice_user_related_name(self):
        user = CustomUser.objects.get(username=self.user1.username)
        invoices = user.invoiceUser.all()
        self.assertEqual(invoices.count(), 1)

    def test_invoice_client_related_name(self):
        user = CustomUser.objects.get(username=self.user2.username)
        invoices = user.invoiceClient.all()
        self.assertEqual(invoices.count(), 1)


class ItemModelTest(TestCase):
    def setUp(self):
        user1 = CustomUser.objects.create(
            company_name='John Doe', email="johndoe@gmail.com", username="johndoe", password="test1234"
        )
        user2 = CustomUser.objects.create(
            company_name='Jane Doe', email="janedoe@gmail.com", username="janedoe", password="test12345"
        )
        invoice = Invoice.objects.create(user=user1, client=user2, invoiceDate='2023-05-13', dueDate='2023-05-20', totalAmount=100.00, dueAmount=50.00, advancePercent=50, workCompleted=False, note='Test note')
        self.newItem = Item.objects.create(description='Test item', quantity=2, price=10.00, discount=20, tax=30, invoice=invoice)

    def test_itemid_is_primary_key(self):
        item = Item.objects.get(itemid=self.newItem.itemid)
        self.assertEqual(item.itemid, self.newItem.itemid)

    def test_description_matches_value(self):
        item = Item.objects.get(itemid=self.newItem.itemid)
        self.assertEqual(item.description, 'Test item')

    def test_quantity_matches_value(self):
        item = Item.objects.get(itemid=self.newItem.itemid)
        self.assertEqual(item.quantity, 2)

    def test_price_matches_value(self):
        item = Item.objects.get(itemid=self.newItem.itemid)
        self.assertEqual(item.price, 10.00)

    def test_discount_matches_value(self):
        item = Item.objects.get(itemid=self.newItem.itemid)
        self.assertEqual(item.discount, 20)

    def test_tax_matches_value(self):
        item = Item.objects.get(itemid=self.newItem.itemid)
        self.assertEqual(item.tax, 30)

    def test_invoice_matches_value(self):
        item = Item.objects.get(itemid=self.newItem.itemid)
        invoice = item.invoice
        self.assertEqual(invoice.user.email, 'johndoe@gmail.com')
        self.assertEqual(invoice.client.email, 'janedoe@gmail.com')
        self.assertEqual(invoice.totalAmount, 100.00)
        self.assertEqual(invoice.dueAmount, 50.00)
        self.assertEqual(invoice.advancePercent, 50)
        self.assertFalse(invoice.workCompleted)
        self.assertEqual(invoice.note, 'Test note')



class InvoiceCreateAPITest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(
            company_name='John Doe', email="johndoe@gmail.com", username="johndoe", password="test1234"
        )
        self.user2 = CustomUser.objects.create(
            company_name='Jane Doe', email="janedoe@gmail.com", username="janedoe", password="test12345"
        )

        token, _ = Token.objects.get_or_create(user=self.user1)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

        self.url = reverse('add-invoice')
        self.payload = {
            'client': self.user2.id,
            'invoiceDate': '2022-05-13',
            'dueDate': '2022-06-13',
            'totalAmount': 1000.0,
            'advancePercent': 20,
            'workCompleted': False,
            'note': 'Some note',
            'items': [
                {
                    "description": "item 1",
                    "quantity": 1,
                    "price": 400,
                    "discount": 20,
                    "tax": 20 
                },
                {
                    "description": "item 2",
                    "quantity": 2,
                    "price": 300,
                    "discount": 20,
                    "tax": 20 
                }
            ]
        }

    def test_create_invoice(self):
        response = self.client.post(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Invoice.objects.count(), 1)
        self.assertEqual(Invoice.objects.get(id=1).user, self.user1)
        self.assertEqual(Invoice.objects.get().client, self.user2)
        self.assertEqual(str(Invoice.objects.get().invoiceDate), '2022-05-13')
        self.assertEqual(str(Invoice.objects.get().dueDate), '2022-06-13')
        self.assertEqual(Invoice.objects.get().totalAmount, 1000.0)
        self.assertEqual(Invoice.objects.get().dueAmount, 1000.0)
        self.assertEqual(Invoice.objects.get().advancePercent, 20)
        self.assertEqual(Invoice.objects.get().workCompleted, False)
        self.assertEqual(Invoice.objects.get().note, 'Some note')



class InvoicesListAPITest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(
            company_name='John Doe', email="johndoe@gmail.com", username="johndoe", password="test1234"
        )
        self.user2 = CustomUser.objects.create(
            company_name='Jane Doe', email="janedoe@gmail.com", username="janedoe", password="test12345"
        )
        self.invoice1 = Invoice.objects.create(user=self.user1, client=self.user2, invoiceDate='2022-05-01', dueDate='2022-06-01', totalAmount=1000.0, dueAmount=800.0, advancePercent=20, workCompleted=False, note='Note 1')
        self.invoice2 = Invoice.objects.create(user=self.user1, client=self.user2, invoiceDate='2022-05-02', dueDate='2022-06-02', totalAmount=2000.0, dueAmount=1600.0, advancePercent=20, workCompleted=True, note='Note 2')

        token, _ = Token.objects.get_or_create(user=self.user1)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)
        self.url = reverse('fetch-invoices')

    def test_get_invoices(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['user'], self.user1.id)
        self.assertEqual(response.data[0]['client'], self.user2.id)
        self.assertEqual(str(response.data[0]['invoiceDate']), '2022-05-01')
        self.assertEqual(str(response.data[0]['dueDate']), '2022-06-01')
        self.assertEqual(response.data[0]['totalAmount'], 1000.0)
        self.assertEqual(response.data[0]['dueAmount'], 800.0)
        self.assertEqual(response.data[0]['advancePercent'], 20)
        self.assertEqual(response.data[0]['workCompleted'], False)
        self.assertEqual(response.data[0]['note'], 'Note 1')
        self.assertEqual(response.data[1]['user'], self.user1.id)
        self.assertEqual(response.data[1]['client'], self.user2.id)
        self.assertEqual(str(response.data[1]['invoiceDate']), '2022-05-02')
        self.assertEqual(str(response.data[1]['dueDate']), '2022-06-02')
        self.assertEqual(response.data[1]['totalAmount'], 2000.0)
        self.assertEqual(response.data[1]['dueAmount'], 1600.0)
        self.assertEqual(response.data[1]['advancePercent'], 20)
        self.assertEqual(response.data[1]['workCompleted'], True)
        self.assertEqual(response.data[1]['note'], 'Note 2')


class InvoiceDetailAPITest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create(
            company_name='John Doe', email="johndoe@gmail.com", username="johndoe", password="test1234"
        )
        self.user2 = CustomUser.objects.create(
            company_name='Jane Doe', email="janedoe@gmail.com", username="janedoe", password="test12345"
        )
        self.invoice1 = Invoice.objects.create(user=self.user1, client=self.user2, invoiceDate='2022-05-01', dueDate='2022-06-01', totalAmount=1000.0, dueAmount=1000.0, advancePercent=20, workCompleted=False, note='Note 1')
        self.invoice2 = Invoice.objects.create(user=self.user2, client=self.user2, invoiceDate='2022-05-02', dueDate='2022-06-02', totalAmount=2000.0, dueAmount=2000.0, advancePercent=20, workCompleted=True, note='Note 2')
        self.item1 = Item.objects.create(description='Item 1', quantity=2, price=100.0, discount=10, tax=18.0, invoice=self.invoice1)
        self.item2 = Item.objects.create(description='Item 2', quantity=1, price=200.0, discount=20, tax=36.0, invoice=self.invoice1)

        token, _ = Token.objects.get_or_create(user=self.user1)                
        self.client = Client(HTTP_AUTHORIZATION='Token ' + token.key)

        self.url = reverse('invoice-detail', args=[self.invoice1.id])
        self.payload = {
            'invoiceDate': '2022-05-01',
            'dueDate': '2022-06-01',
            'totalAmount': 1200.0,
            'advancePercent': 10,
            'workCompleted': True,
            'note': 'Some note',
        }

    def test_get_invoice_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], self.user1.id)
        self.assertEqual(response.data['client'], self.user2.id)
        self.assertEqual(str(response.data['invoiceDate']), '2022-05-01')
        self.assertEqual(str(response.data['dueDate']), '2022-06-01')
        self.assertEqual(response.data['totalAmount'], 1000.0)
        self.assertEqual(response.data['dueAmount'], 1000.0)
        self.assertEqual(response.data['advancePercent'], 20)
        self.assertEqual(response.data['workCompleted'], False)
        self.assertEqual(response.data['note'], 'Note 1')
        self.assertEqual(len(response.data['items']), 2)
        self.assertEqual(response.data['items'][0]['description'], 'Item 1')
        self.assertEqual(response.data['items'][0]['quantity'], 2)
        self.assertEqual(response.data['items'][0]['price'], 100.0)
        self.assertEqual(response.data['items'][0]['discount'], 10)
        self.assertEqual(response.data['items'][0]['tax'], 18.0)
        self.assertEqual(response.data['items'][1]['description'], 'Item 2')
        self.assertEqual(response.data['items'][1]['quantity'], 1)
        self.assertEqual(response.data['items'][1]['price'], 200.0)
        self.assertEqual(response.data['items'][1]['discount'], 20)
        self.assertEqual(response.data['items'][1]['tax'], 36.0)

    def test_update_invoice_details(self):
        response = self.client.patch(
            self.url,
            data=json.dumps(self.payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.invoice1.refresh_from_db()
        self.assertEqual(self.invoice1.client, self.user2)
        self.assertEqual(str(self.invoice1.invoiceDate), '2022-05-01')
        self.assertEqual(str(self.invoice1.dueDate), '2022-06-01')
        self.assertEqual(self.invoice1.totalAmount, 1200.0)
        self.assertEqual(self.invoice1.dueAmount, 1000.0)
        self.assertEqual(self.invoice1.advancePercent, 10)
        self.assertEqual(self.invoice1.workCompleted, True)
        self.assertEqual(self.invoice1.note, 'Some note')
