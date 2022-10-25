from rest_framework import serializers

from .models import Customer
from invoice.models import Invoice

class CustomerInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = (
            "id",
            "invoice_number",
            "is_sent",
            "is_paid",
            "gross_amount",
            "vat_amount",
            "net_amount",
            "get_due_date_formatted",
            "invoice_type",
            "is_credited",
        )

class CustomerSerializer(serializers.ModelSerializer):   
    invoices = CustomerInvoiceSerializer(many=True, required=False)

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
            "invoices",
        )
