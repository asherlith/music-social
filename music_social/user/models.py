from django.contrib.auth.models import User
from django.db import models
from reusable.models import BaseModel
from reusable.file_path import Path
# Create your models here.


class Profile(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nick_name = models.CharField(max_length=200)
    bio = models.TextField()
    image = models.ImageField(upload_to=Path.user_profile_image_path)
