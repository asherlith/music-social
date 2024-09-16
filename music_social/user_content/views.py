from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from user_content.models import ProfilePost
from user_content.serializers import ProfilePostSerializer


class UploadContentView(APIView):
    def post(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            profile = request.user.profile

            request.data.file = request.FILES
            validate_data = ProfilePostSerializer(data=request.data)

            if validate_data.is_valid():
                data = validate_data.validated_data
                obj = ProfilePost.objects.create(profile=profile, **data)

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

            return Response(
                ProfilePostSerializer(
                    posts,
                    many=True,
                    context={'request': request}
                ).data,
                status=status.HTTP_200_OK
            )
