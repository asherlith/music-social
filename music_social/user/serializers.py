from rest_framework import serializers

from user.models import Profile
from user_content.models import ProfileSong


class ProfileInputSerializer(serializers.Serializer):
    biography = serializers.CharField(required=False)
    profile_picture = serializers.ImageField(required=False)
    biography_song = serializers.IntegerField(required=False)
    biography_song_start_second = serializers.IntegerField(required=False)
    biography_song_end_second = serializers.IntegerField(required=False)
    nickname = serializers.CharField(required=False)


class BiographySongSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProfileSong
        fields = ['song', 'biography_song_start_second', 'biography_song_end_second']


class ProfileSerializer(serializers.ModelSerializer):
    biography_song = BiographySongSerializer(required=False)

    class Meta:
        model = Profile
        fields = ['biography', 'profile_picture', 'biography_song', 'nickname']
