from sys import base_prefix

from django.db import models

from reusable.models import BaseModel
from utilities.path import audio_path, audio_cover_path


class Album(BaseModel):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class Artist(BaseModel):
    name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    def __str__(self):
        return self.name


class Song(BaseModel):
    name = models.CharField(max_length=120)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    album = models.ForeignKey('Album', on_delete=models.CASCADE)
    audio = models.FileField(
        upload_to=audio_path,
        null=True,
        blank=True
    )
    cover = models.ImageField(
        upload_to=audio_cover_path,
        null=True,
        blank=True,
    )
    enable = models.BooleanField(default=True)
    duration = models.FloatField(default=0)
    times = models.CharField(blank=True, null=True)
    energy = models.CharField(blank=True, null=True)
    def __str__(self):
        return self.name