from django.contrib.auth.models import AbstractUser
from django.db import models

from content.models import Artist
from reusable.models import BaseModel
from user_content.models import ProfileSong
from utilities.path import profile_avatar_path, profile_colors_path


# Create your models here.

class User(AbstractUser):
    verified = models.BooleanField(default=False)


class Profile(BaseModel):
    biography = models.TextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follower = models.ManyToManyField('self', related_name='follower_users',symmetrical=False, null=True, blank=True)
    following = models.ManyToManyField('self', related_name='following_users',symmetrical=False, null=True, blank=True)
    profile_picture = models.ImageField(upload_to=profile_avatar_path, null=True, blank=True)
    biography_song = models.ForeignKey(ProfileSong, related_name='user_profile', on_delete=models.SET_NULL, null=True, blank=True)
    nickname = models.CharField(max_length=120)
    statistics = models.ImageField(upload_to=profile_colors_path, null=True, blank=True)




class ArtistProfile(Profile):
    artist = models.OneToOneField(Artist, on_delete=models.CASCADE)
