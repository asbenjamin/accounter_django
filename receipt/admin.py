from django.contrib import admin

from .models import Receipt, SaleItem

admin.site.register(Receipt)
admin.site.register(SaleItem)
