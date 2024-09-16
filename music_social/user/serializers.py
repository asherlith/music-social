from rest_framework import serializers

from user.models import Profile, User
from user_content.models import ProfileSong

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]


class ProfileInputSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

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
    biography_song = serializers.SerializerMethodField()
    post_count = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    follower = serializers.SerializerMethodField()

    user = UserSerializer()

    class Meta:
        model = Profile

        fields = ['biography', 'profile_picture', 'biography_song', 'nickname', 'user', 'follower', 'following', 'post_count']

    def get_biography_song(self, instance):
        return BiographySongSerializer(instance.profile_song.last()).data

    def get_post_count(self, instance):
        return instance.posts.filter(is_main=True).count()

    def get_following(self, instance):
        return instance.following.all().count() if instance.following else 0

    def get_follower(self, instance):
        return instance.follower.all().count() if instance.follower else 0

