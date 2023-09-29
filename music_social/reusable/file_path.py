from os import path

from django.core.exceptions import ValidationError
from django.utils import timezone


class Path:
    def user_profile_image_path(instance, filename):
        # TODO
        # Assuming the image field is named 'image'
        return f'user_{instance.user.id}/{filename}'
