from django.db import models

from content.models import Song
from reusable.models import BaseModel
from utilities.path import profile_post_path


class ProfileSong(BaseModel):
    profile = models.OneToOneField('user.Profile', on_delete=models.CASCADE)
    song = models.OneToOneField('content.Song', on_delete=models.CASCADE)
    biography_song_start_second = models.IntegerField()
    biography_song_end_second = models.IntegerField()

    def __str__(self):
        return self.song.name


class ProfilePost(BaseModel):
    profile = models.ForeignKey('user.Profile', on_delete=models.CASCADE)
    file = models.FileField(upload_to=profile_post_path)
    audio = models.ForeignKey(Song, on_delete=models.CASCADE)
    audio_start = models.FloatField(default=0)
    audio_end = models.FloatField(default=0)
    caption = models.TextField(blank=True)
    is_archive = models.BooleanField(default=False)
    is_daily = models.BooleanField(default=False)
    is_main = models.BooleanField(default=False)
    is_color = models.BooleanField(default=False)
