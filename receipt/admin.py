from django.contrib import admin

from .models import Item, Receipt

admin.site.register(Receipt)
admin.site.register(Item)
