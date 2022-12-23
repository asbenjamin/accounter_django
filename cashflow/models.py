from django.db import models


class Funding(models.Model):
    source = models.CharField(max_length=100, blank=True, null=True, default="")
    contributor_name = models.CharField(max_length=100, default="")
    contributor_org = models.CharField(max_length=100, default="")
    date_received = models.DateField(default="")
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0)


class Equity(models.Model):
    class Source(models.TextChoices):
        INHOUSE = "INHOUSE"
        EXTERNAL = "EXTERNAL"

    source=models.CharField(max_length=15, choices=Source.choices, default=Source.INHOUSE)
    contributor_name = models.CharField(max_length=100, default="")
    contributor_org = models.CharField(max_length=100, default="")
    date_received = models.DateField(default="")
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0)


class OpeningBalance(models.Model):
    opening_date = models.DateField(default="")
    amount = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, default=0)
