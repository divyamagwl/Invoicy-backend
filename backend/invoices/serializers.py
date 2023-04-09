from rest_framework import serializers, fields

from .models import Invoice, Item

class ItemSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Item
        fields = ('itemid', 'description', 'quantity', 'price', 'discount', 'tax')

class InvoiceCreateSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")
    items = ItemSerializer(many=True)
    invoiceDate = fields.DateField(input_formats=['%Y-%m-%d'])
    dueDate = fields.DateField(input_formats=['%Y-%m-%d'])

    class Meta:
        model = Invoice
        fields = ('id', 'user', 'client', 'invoiceDate', 'dueDate', 'totalAmount', 'advancePercent', 'note', 'items')

    def create(self, validated_data):
        validated_data["dueAmount"] = validated_data.get("totalAmount")
        validated_data["workCompleted"] = False
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)
        for item_data in items_data:
            Item.objects.create(invoice=invoice, **item_data)
        return invoice
    
class InvoiceDetailsSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Invoice
        fields = ('id', 'user', 'client', 'invoiceDate', 'dueDate', 
                  'totalAmount', 'dueAmount', 'advancePercent', 'workCompleted', 'note', 'items')
        read_only_fields = ('id', 'user', 'client', 'items')