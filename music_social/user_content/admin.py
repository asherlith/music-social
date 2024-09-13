from django.contrib import admin

from user_content.models import ProfilePost


@admin.register(ProfilePost)
class ProfilePostAdmin(admin.ModelAdmin):
    pass