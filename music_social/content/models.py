from django.db import models

from reusable.models import BaseModel


# Create your models here.


class Album(BaseModel):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class Artist(BaseModel):
    name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)


class Song(BaseModel):
    name = models.CharField(max_length=120)
    artist = models.ForeignKey('Artist', on_delete=models.CASCADE)
    album = models.ForeignKey('Album', on_delete=models.CASCADE)