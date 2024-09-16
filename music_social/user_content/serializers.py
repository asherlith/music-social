from rest_framework import serializers

from content.serializers import SongSerializer
from user_content.models import ProfilePost



class ProfileInputPostSerializer(serializers.ModelSerializer):
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

class ProfilePostSerializer(serializers.ModelSerializer):
    audio = SongSerializer()
    class Meta:
        model = ProfilePost
        fields = (
            'id',
            'file',
            'audio',
            'caption',
            'is_archive',
            'is_daily',
            'is_main',
            'audio_start',
            'audio_end',
            'palette'
        )