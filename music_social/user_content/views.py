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
