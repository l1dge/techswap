from django.contrib import admin
from itemmgmt.models import Items, Photos, Categories, Location


class ItemsAdmin(admin.ModelAdmin):
    pass


admin.site.register(Items, ItemsAdmin)


class PhotosAdmin(admin.ModelAdmin):
    pass


admin.site.register(Photos, PhotosAdmin)


class CategoriesAdmin(admin.ModelAdmin):
    pass


admin.site.register(Categories, CategoriesAdmin)


class LocationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Location, LocationAdmin)
