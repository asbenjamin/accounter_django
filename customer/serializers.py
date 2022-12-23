from rest_framework import serializers

from .models import Customer
from receipt.models import Receipt

class CustomerReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = (
            "id",
            "receipt_number",
            "is_sent",
            "is_paid",
            "gross_amount",
            "vat_amount",
            "net_amount",
            "get_due_date_formatted",
            "receipt_type",
            "is_credited",
        )

class CustomerSerializer(serializers.ModelSerializer):   
    receipts = CustomerReceiptSerializer(many=True, required=False)

    class Meta:
        model = Customer
        read_only_fields = (
            "created_at",
            "created_by",
        ),
        fields = (
            "id",
            "name",
            "email",
            "org_number",
            "address1",
            "address2",
            "zipcode",
            "place",
            "country",
            "contact_person",
            "contact_reference",
            "receipts",
        )
