import os
from django.utils import timezone


def audio_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    return os.path.join(
        ".", "audio", "files", "{}.{}".format(int(timezone.now().timestamp()), ext)
    )

def audio_cover_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    return os.path.join(
        ".", "audio", "cover", "{}.{}".format(int(timezone.now().timestamp()), ext)
    )

def profile_post_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    p_id = f"{instance.profile.id}"
    return os.path.join(
        ".", "profile", p_id, "posts", "{}.{}".format(int(timezone.now().timestamp()), ext)
    )

def profile_avatar_path(instance, filename):
    ext = filename.split(".")[-1].lower()
    p_id = f"{instance.id}"
    return os.path.join(
        ".", "avatars", p_id, "{}.{}".format(int(timezone.now().timestamp()), ext)
    )