from django.contrib import admin
from usermgmt.models import Feedback, Profile

class ProfileAdmin(admin.ModelAdmin):
    pass
admin.site.register(Profile, ProfileAdmin)

