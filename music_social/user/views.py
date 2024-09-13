import random
import string

from django.contrib.auth.hashers import check_password
from django.core.cache import cache
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView

from user.models import User, Profile
from user.serializers import ProfileInputSerializer, ProfileSerializer
from user_content.models import ProfileSong


def generate_random_otp():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def generate_random_username():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


def generate_random_password():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))


def send_email(email, otp):
    from django.core import mail
    from django.conf import settings
    with mail.get_connection() as connection:
        mail.EmailMessage(
            subject='otp',
            body=f'here is your otp : {otp}',
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
            connection=connection,
        ).send()


class LoginView(APIView):
    def get(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = User.objects.filter(username=username).first()
        token = Token.objects.filter(user=user).first()
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if check_password(password, user.password):
            return Response({'token': str(token)}, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        if not User.objects.filter(email=email, verified=True).exists():

            if not User.objects.filter(username=email).exists():
                user = User.objects.create_user(username=email, email=email)
                token = Token.objects.create(user=user)
            else:
                user = User.objects.filter(username=email).first()
                token = Token.objects.filter(user=user).first()

            if not cache.get(f'{email}'):
                user_otp = generate_random_otp()
                cache.set(f'{email}', user_otp, 2*60)
            else:
                user_otp = cache.get(f'{email}')

            send_email(email, user_otp)
            return Response({'token': str(token)}, status=status.HTTP_201_CREATED)

        else:
            return Response({'error': 'Error'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        if request.user.is_authenticated:
            email = request.user.username
            user = User.objects.filter(username=email).first()
            user_ = User.objects.filter(username=username).first()
            if not user or user_:
                return Response(status=status.HTTP_404_NOT_FOUND)
            else:
                user.set_password(password)
                user.username = username
                Profile.objects.create(user=user)
                user.save()
                return Response(status=status.HTTP_200_OK)

        return Response({'error': 'Error'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterVerifyView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user
        entered_otp = data.get('entered_otp')

        if user.is_authenticated:
            if not cache.get(f'{user.username}'):
                return Response('OTP expired/User doesnt exist', status=status.HTTP_400_BAD_REQUEST)

            elif cache.get(f'{user.username}') != entered_otp:
                return Response({'error': 'OTP did not match'}, status=status.HTTP_400_BAD_REQUEST)

            else:
                user.verified = True
                user.save()
                return Response('OTP verified', status=status.HTTP_200_OK)

        else:
            return Response({'error': 'User doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    def get(self, request, *args, **kwargs):
        data = request.data

        if not request.GET.get('second'):
            email = data.get('email')
            if User.objects.filter(email=email, verified=True).exists():
                if not cache.get(f'reset-{email}'):
                    user_otp = generate_random_otp()
                    cache.set(f'reset-{email}', user_otp, 60*60)
                else:
                    user_otp = cache.get(f'reset-{email}')

                send_email(email, user_otp)
                return Response(status=status.HTTP_200_OK)

            return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            otp = data.get('otp')
            email = data.get('email')
            password = data.get('password')
            user = User.objects.filter(email=email).first()
            if not user:
                return Response(status=status.HTTP_404_NOT_FOUND)
            if not password:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if cache.get(f'reset-{email}'):

                if otp == cache.get(f'reset-{email}'):
                    user.set_password(password)
                    user.save()
                    return Response(status=status.HTTP_200_OK)

                return Response({'error': 'OTP did not match'}, status=status.HTTP_400_BAD_REQUEST)

            return Response(status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def patch(self, request, *args, **kwargs):
        data = request.data

        if ProfileInputSerializer(**data).is_valid():
            data = ProfileInputSerializer(**data).data
            if "biography_song" in data.keys():
                ProfileSong.objects.create(
                    profile=request.user.profile,
                    song=data.get('song'),
                    biography_song_start_second=data.get('biography_song_start_second'),
                    biography_song_end_second=data.get('biography_song_end_second')

                )
            Profile.objects.update(**data)

    def get(self, request, *args, **kwargs):
        return Response(ProfileSerializer(request.user.profile).data, status=status.HTTP_200_OK)




