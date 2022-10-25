import decimal

from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models

from customer.models import Customer
from team.models import Team

class Receipt(models.Model):
    RECEIPT = 'receipt'
    CREDIT_NOTE = 'credit_note'

    CHOICES_TYPE = (
        (RECEIPT, 'receipt'),
        (CREDIT_NOTE, 'Credit note')
    )

    receipt_number = models.IntegerField(default=1)
    customer_name = models.CharField(max_length=255)
    customer_email = models.CharField(max_length=255)
    customer_org_number = models.CharField(max_length=255, blank=True, null=True)
    customer_address1 = models.CharField(max_length=255, blank=True, null=True)
    customer_address2 = models.CharField(max_length=255, blank=True, null=True)
    customer_zipcode = models.CharField(max_length=255, blank=True, null=True)
    customer_place = models.CharField(max_length=255, blank=True, null=True)
    customer_country = models.CharField(max_length=255, blank=True, null=True)
    customer_contact_person = models.CharField(max_length=255, blank=True, null=True)
    customer_contact_reference = models.CharField(max_length=255, blank=True, null=True)
    sender_reference = models.CharField(max_length=255, blank=True, null=True)
    receipt_type = models.CharField(max_length=20, choices=CHOICES_TYPE, default=RECEIPT)
    due_days = models.IntegerField(default=14)
    is_credit_for = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    is_credited = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)
    bankaccount = models.CharField(max_length=266, blank=True, null=True)
    gross_amount = models.DecimalField(max_digits=6, decimal_places=2)
    vat_amount = models.DecimalField(max_digits=6, decimal_places=2)
    net_amount = models.DecimalField(max_digits=6, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=6, decimal_places=2)
    team = models.ForeignKey(Team, related_name='receipts', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='receipts', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='created_receipts', on_delete=models.CASCADE)
    modified_by = models.ForeignKey(User, related_name='modified_receipts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
    
    def get_due_date(self):
        return self.created_at + timedelta(days=self.due_days)
    
    def get_due_date_formatted(self):
        return self.get_due_date().strftime("%d.%m.%Y")

class Item(models.Model):
    receipt = models.ForeignKey(Receipt, related_name='items', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    net_amount = models.DecimalField(max_digits=6, decimal_places=2)
    vat_rate = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)

    def get_gross_amount(self):
        vat_rate = decimal.Decimal(self.vat_rate/100)
        return self.net_amount + (self.net_amount * vat_rate)

    def save(self, *args, **kwargs):
        self.net_amount = self.quantity * self.unit_price
        return super(Item, self).save()
