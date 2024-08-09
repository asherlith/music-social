from django.db import models

from content.models import Song
from reusable.models import BaseModel
from user.models import Profile


class ProfileSong(BaseModel):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    song = models.OneToOneField(Song, on_delete=models.CASCADE)
    biography_song_start_second = models.IntegerField()
    biography_song_end_second = models.IntegerField()

    def __str__(self):
        return self.song.name


class ProfilePost(BaseModel):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    file = models.FileField(upload_to='profiles/')
    audio = models.ForeignKey(Song, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    is_archive = models.BooleanField(default=False)
    is_daily = models.BooleanField(default=False)
    is_main = models.BooleanField(default=False)
    is_color = models.BooleanField(default=False)

    def __str__(self):
        return self.profile.name