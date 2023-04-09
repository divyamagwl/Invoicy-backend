from django.db import models
from users.models import CustomUser

class Invoice(models.Model):
    user = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='invoiceUser')
    client = models.ForeignKey(CustomUser, null=False, on_delete=models.CASCADE, related_name='invoiceClient')
    invoiceDate = models.DateField()
    dueDate = models.DateField()
    totalAmount = models.FloatField()
    dueAmount = models.FloatField()   
    advancePercent = models.IntegerField()
    workCompleted = models.BooleanField()
    note = models.CharField(max_length=200)

class Item(models.Model):
    itemid = models.AutoField(primary_key=True)
    description = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.FloatField()
    discount = models.IntegerField()
    tax = models.FloatField()
    invoice = models.ForeignKey(Invoice, null=False, on_delete=models.CASCADE, related_name='items')
