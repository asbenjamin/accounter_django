# Generated by Django 4.1 on 2022-10-31 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('receipt', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Item',
            new_name='SaleItem',
        ),
    ]
