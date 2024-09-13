from django.contrib import admin
from .models import Album, Artist, Song
# Register your models here.

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    ...


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    ...


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'album', 'enable')
    list_filter = ('artist', 'album', 'enable')