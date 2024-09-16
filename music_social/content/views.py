from celery.bin.control import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response

from content.models import Song
from content.serializers import SongSerializer


class SongsView(ListAPIView):
    serializer_class = SongSerializer
    queryset = Song.objects.filter(enable=True).exclude(audio="")

    def get(self, request,*args,**kwargs):
        if request.GET.get('search'):
            return Response(
                self.serializer_class(self.queryset.filter(name__icontains=request.GET.get('search')), many=True).data, status=200)
        else:
            return super().get(request,*args, **kwargs)


class SongsDetailView(RetrieveAPIView):
    queryset = Song.objects.all()  # The queryset for retrieving Song instances
    serializer_class = SongSerializer  # The serializer to use for representing Song data
    lookup_field = 'id'  #
