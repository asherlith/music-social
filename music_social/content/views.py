from rest_framework.generics import ListAPIView

from content.models import Song
from content.serializers import SongSerializer


class SongsView(ListAPIView):
    serializer_class = SongSerializer
    queryset = Song.objects.filter(enable=True).exclude(audio="")