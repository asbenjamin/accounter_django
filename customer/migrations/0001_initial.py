# Generated by Django 4.1 on 2022-10-25 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('org_number', models.CharField(blank=True, max_length=255, null=True)),
                ('address1', models.CharField(blank=True, max_length=255, null=True)),
                ('address2', models.CharField(blank=True, max_length=255, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=255, null=True)),
                ('place', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_person', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_reference', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customers', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
