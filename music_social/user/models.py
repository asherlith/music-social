from django.contrib.auth.models import User
from django.db import models

from content.models import Artist
from reusable.models import BaseModel
from reusable.file_path import Path
from user_content.models import ProfileSong


# Create your models here.


class Profile(BaseModel):
    biography = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follower = models.ForeignKey('self', related_name='followers', null=True, blank=True, on_delete=models.SET_NULL)
    following = models.ForeignKey('self', related_name='following', null=True, blank=True, on_delete=models.SET_NULL)
    profile_picture = models.FileField(upload_to=Path, null=True, blank=True)
    biography_song = models.ForeignKey(ProfileSong, on_delete=models.SET_NULL, null=True, blank=True)
    nickname = models.CharField(max_length=120)
    def __str__(self):
        return self.user.username


class ArtistProfile(Profile):
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)
