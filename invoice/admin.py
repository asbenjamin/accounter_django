from django.contrib import admin

from .models import Invoice, ExpenseItem

admin.site.register(Invoice)
admin.site.register(ExpenseItem)
