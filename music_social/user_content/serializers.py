from rest_framework import serializers

from user_content.models import ProfilePost


class ProfilePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePost
        fields = (
            'file',
            'audio',
            'caption',
            'is_archive',
            'is_daily',
            'is_main',
            'audio_start',
            'audio_end',
        )