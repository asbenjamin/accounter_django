from rest_framework import serializers

from .models import Receipt, SaleItem

class ItemSerializer(serializers.ModelSerializer):   
    class Meta:
        model = SaleItem
        read_only_fields = (
            "receipt",
        )
        fields = (
            "id",
            "title",
            "quantity",
            "unit_price",
            "net_amount",
            "vat_rate",
            "discount",
        )

class ReceiptSerializer(serializers.ModelSerializer):   
    items = ItemSerializer(many=True)
    bankaccount = serializers.CharField(required=False)

    class Meta:
        model = Receipt
        read_only_fields = (
            "team",
            "receipt_number",
            "created_at",
            "created_by",
            "modified_at",
            "modified_by",
        ),
        fields = (
            "id",
            "receipt_number",
            "customer",
            "customer_name",
            "customer_email",
            "customer_org_number",
            "customer_address1",
            "customer_address2",
            "customer_zipcode",
            "customer_place",
            "customer_country",
            "customer_contact_person",
            "customer_contact_reference",
            "sender_reference",
            "receipt_type",
            "due_days",
            "is_sent",
            "is_paid",
            "gross_amount",
            "vat_amount",
            "net_amount",
            "discount_amount",
            "items",
            "bankaccount",
            "get_due_date_formatted",
            "is_credit_for",
            "is_credited",
        )
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        receipt = Receipt.objects.create(**validated_data)

        for item in items_data:
            SaleItem.objects.create(receipt=receipt, **item)
        
        return receipt
