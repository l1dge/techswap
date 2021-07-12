from django.contrib import admin
from .models import *


class ItemsAdmin(admin.ModelAdmin):
    pass


admin.site.register(
    [Item, ItemImage, Category, Location],
    ItemsAdmin,
)


class SwapAdmin(admin.ModelAdmin):
    pass


admin.site.register(
    [Swap, SwapList, SwapListItem, WishList, WishListItem],
    SwapAdmin,
)


# class ForSwapAdmin(admin.ModelAdmin):
#     pass


# admin.site.register(ForSwap, ForSwapAdmin)


class ProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register([Profile, Address], ProfileAdmin)
