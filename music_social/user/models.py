from django.contrib.auth.models import AbstractUser
from django.db import models

from content.models import Artist
from reusable.models import BaseModel
from reusable.file_path import Path
from user_content.models import ProfileSong
from utilities.path import profile_avatar_path


# Create your models here.

class User(AbstractUser):
    verified = models.BooleanField(default=False)


class Profile(BaseModel):
    biography = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follower = models.ForeignKey('self', related_name='follower_users', null=True, blank=True, on_delete=models.SET_NULL)
    following = models.ForeignKey('self', related_name='following_users', null=True, blank=True, on_delete=models.SET_NULL)
    profile_picture = models.ImageField(upload_to=profile_avatar_path, null=True, blank=True)
    biography_song = models.ForeignKey(ProfileSong, related_name='user_profile', on_delete=models.SET_NULL, null=True, blank=True)
    nickname = models.CharField(max_length=120)




class ArtistProfile(Profile):
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)
