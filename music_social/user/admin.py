from django.contrib import admin

from user.models import User, Profile


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ...

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    ...