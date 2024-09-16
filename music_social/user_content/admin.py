from django.contrib import admin

from user_content.models import ProfilePost, ProfileSong


@admin.register(ProfilePost)
class ProfilePostAdmin(admin.ModelAdmin):
    pass


@admin.register(ProfileSong)
class ProfileSongAdmin(admin.ModelAdmin):
    pass