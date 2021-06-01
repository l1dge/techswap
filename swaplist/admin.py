from django.contrib import admin
from swaplist.models import Wanted, ForSwap


class WantedAdmin(admin.ModelAdmin):
    pass


admin.site.register(Wanted, WantedAdmin)


class ForSwapAdmin(admin.ModelAdmin):
    pass


admin.site.register(ForSwap, ForSwapAdmin)
