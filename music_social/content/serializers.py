from rest_framework import serializers

from content.models import Song, Artist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = [
            'name'
        ]
class SongSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
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