from rest_framework import serializers

from .models import Client
from invoice.models import Invoice

class ClientInvoiceSerializer(serializers.ModelSerializer):
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

class ClientSerializer(serializers.ModelSerializer):   
    invoices = ClientInvoiceSerializer(many=True, required=False)

    class Meta:
        model = Client
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

    def update(self, instance, validated_data):
        # clients = validated_data.pop('clients')

        instance = self.context.get("request").id

        print("instance============================", instance)

        # instance.name = validated_data.get('name', instance.name)
        # instance.save()

        # many contacts
        # for client in clients:
        this_client = Client.objects.get(instance) # this will crash if the id is invalid though
        print(this_client)
        this_client.name = validated_data.get('name', instance.name)
        this_client.email = validated_data.get('email', instance.email)
        this_client.org_number = validated_data.get('org_number', instance.org_number)
        this_client.address1 = validated_data.get('address1', instance.address1)
        this_client.address2 = validated_data.get('address2', instance.address2)
        this_client.zipcode = validated_data.get('zipcode', instance.zipcode)
        this_client.place = validated_data.get('place', instance.place)
        this_client.country = validated_data.get('country', instance.country)
        this_client.contact_person = validated_data.get('contact_person', instance.contact_person)
        this_client.contact_reference = validated_data.get('contact_reference', instance.contact_reference)
        this_client.receipts = validated_data.get('receipts', instance.receipts)
        this_client.save()

        return instance
