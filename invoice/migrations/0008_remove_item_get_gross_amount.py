# Generated by Django 4.1 on 2022-10-24 19:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0007_item_get_gross_amount_alter_invoice_id_alter_item_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='get_gross_amount',
        ),
    ]
