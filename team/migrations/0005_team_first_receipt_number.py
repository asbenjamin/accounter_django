# Generated by Django 4.1 on 2022-10-31 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0004_alter_team_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='first_receipt_number',
            field=models.IntegerField(default=1),
        ),
    ]
