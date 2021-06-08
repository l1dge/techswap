from django.contrib import admin
from .models import *


class ItemsAdmin(admin.ModelAdmin):
    pass


admin.site.register([Item, ItemImage, Category, Location], ItemsAdmin)


class WantedAdmin(admin.ModelAdmin):
    pass


admin.site.register(Wanted, WantedAdmin)


class ForSwapAdmin(admin.ModelAdmin):
    pass


admin.site.register(ForSwap, ForSwapAdmin)


class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
