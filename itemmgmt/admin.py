from django.contrib import admin
from itemmgmt.models import Item, ItemImage, Category, Location


class ItemsAdmin(admin.ModelAdmin):
    pass


admin.site.register([Item, ItemImage, Category, Location], ItemsAdmin)
