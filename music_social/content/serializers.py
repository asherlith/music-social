from rest_framework import serializers

from content.models import Song


class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = [
            'id',
            'name',
            'artist',
            'album',
            'audio',
            'cover',
            'duration'
        ]