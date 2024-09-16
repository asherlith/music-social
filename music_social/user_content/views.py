import ast
import json

import librosa
import numpy as np

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from user_content.models import ProfilePost
from user_content.serializers import ProfilePostSerializer, ProfileInputPostSerializer

from colorthief import ColorThief

from PIL import Image

from utilities.audio_interpreter import handle_graph


def normalize_color(color):
    """Convert a tuple of (r, g, b) from 0-255 to 0-1 range."""
    return tuple(c / 255 for c in color)


def is_image(file_path):
    try:
        img = Image.open(file_path)
        img.verify()
        return True
    except (IOError, SyntaxError):
        return False

class UploadContentView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            profile = request.user.profile

            request.data.file = request.FILES
            validate_data = ProfileInputPostSerializer(data=request.data)

            if validate_data.is_valid():
                data = validate_data.validated_data
                obj = ProfilePost.objects.create(profile=profile, **data)

                if is_image(data.get('file')):
                    color_thief = ColorThief(data.get('file'))
                    palette = color_thief.get_palette(color_count=5, quality=1)
                    obj.palette = palette
                    obj.save()

                return Response(ProfilePostSerializer(obj, context={'request':request}).data, status=status.HTTP_200_OK)
            return Response({'error': 'invalid data'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'error': 'log in'}, status=status.HTTP_400_BAD_REQUEST)

class GetContentView(APIView):
    def get(self, request, *args, **kwargs):
        is_main = request.GET.get('is_main') == 'true'
        is_archive = request.GET.get('is_archive') == 'true'
        is_daily = request.GET.get('is_daily') == 'true'
        user = request.user

        if not user.is_anonymous:
            posts = ProfilePost.objects.filter(profile=user.profile)

            if is_main:
                posts = posts.filter(is_main=True)
            if is_archive:
                posts = posts.filter(is_archive=True)
            if is_daily:
                posts = posts.filter(is_daily=True)
            # post = posts.first()
            #
            # y, sr = librosa.load(post.audio.audio.path)
            # energy = json.loads(post.audio.energy)
            # rms_energy = np.array(energy)
            # handle_graph(rms_energy, [normalize_color(c) for c in ast.literal_eval(post.palette)], y, sr)
            return Response(
                ProfilePostSerializer(
                    posts,
                    many=True,
                    context={'request': request}
                ).data,
                status=status.HTTP_200_OK
            )

class DeleteContentView(APIView):
    def delete(self, request, *args, **kwargs):
        d_id = kwargs.get('id')
        if ProfilePost.objects.filter(profile=request.user.profile,id=d_id).exists():
            ProfilePost.objects.filter(profile=request.user.profile, id=d_id).last().delete()
            return Response({'error': 'error'}, status=200)

        return Response({'error':'error'}, status=400)
