import random
import string

from django.contrib.auth.hashers import check_password
from django.core.cache import cache
from django.db.models import Q, Prefetch, Count, F
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from user.models import User, Profile
from user.serializers import ProfileInputSerializer, ProfileSerializer
from user_content.models import ProfileSong
from utilities.audio_interpreter import get_user_color_stats, generate_statistics, plot_color_distribution


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
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get('username')
        password = data.get('password')
        user = User.objects.filter(Q(username=username)|Q(email=username)).first()

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
        entered_otp = data.get('entered_otp')
        email = data.get('email')
        user = User.objects.filter(email=email).last()


        if not cache.get(f'{user.username}'):
            return Response('OTP expired/User doesnt exist', status=status.HTTP_400_BAD_REQUEST)

        elif cache.get(f'{user.username}') != entered_otp:
            return Response({'error': 'OTP did not match'}, status=status.HTTP_400_BAD_REQUEST)

        else:
            user.verified = True
            user.save()
            return Response('OTP verified', status=status.HTTP_200_OK)



class ResetPasswordView(APIView):
    def post(self, request, *args, **kwargs):
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
                return Response({}, status=status.HTTP_200_OK)

            return Response({}, status=status.HTTP_401_UNAUTHORIZED)

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
                    return Response({}, status=status.HTTP_200_OK)

                return Response({'error': 'OTP did not match'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({}, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def patch(self, request, *args, **kwargs):
        data = request.data
        request.data.profile_picture = request.FILES.get('profile_picture')
        ser = ProfileInputSerializer(data=data, context={'request':request})
        if ser.is_valid():
            data = ser.validated_data

            if data.get('first_name'):
                request.user.first_name = data.pop('first_name')


            if data.get('last_name'):
                request.user.last_name = data.pop('last_name')

            if data.get('username'):
                request.user.username = data.pop('username')
            request.user.save()

            if "biography_song" in data.keys():
                ProfileSong.objects.create(
                    profile=request.user.profile,
                    song_id=data.pop('biography_song'),
                    biography_song_start_second=data.pop('biography_song_start_second'),
                    biography_song_end_second=data.pop('biography_song_end_second')

                )
            Profile.objects.update(**data)
            request.user.profile.profile_picture = request.FILES.get('profile_picture')
            request.user.profile.save()
            return Response({}, status=status.HTTP_200_OK)

        return Response({'error':'invalid data'}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return Response(ProfileSerializer(request.user.profile, context={'request':request}).data, status=status.HTTP_200_OK)



class ProfileSearchView(APIView):
    def get(self, request, *args, **kwargs):
        users=User.objects.filter(username__icontains=request.GET.get('username')).exclude(username=request.user.username).values_list('id', flat=True)
        profiles = Profile.objects.filter(user__in=users)
        return Response(ProfileSerializer(profiles, many=True, context={'request':request}).data, status=status.HTTP_200_OK)



class ProfileUsernameView(APIView):
    def get(self, request, *args, **kwargs):
        username = kwargs.get('username')
        user_ = User.objects.filter(username=username).first()
        if user_:
            return Response(ProfileSerializer(user_.profile, context={'request':request, 'username':user_}).data, status=200)
        else:
            return Response({}, status=400)


class ProfileStatisticsView(APIView):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('username')
        if not request.user.is_anonymous:
            if User.objects.filter(username=username):
                user = User.objects.filter(username=username).last()
            else:
                user = request.user
            get_user_color_stats(user.id)
            stats = generate_statistics(user.id)
            plot_color_distribution(stats, request.user.profile, 'statistics')
            return Response({'image_url':request.build_absolute_uri(request.user.profile.statistics).replace("user/profile/statistics/", "media/")}, status=200)
        return Response({'error':'error'}, status=400)


class ProfileSearchRandomView(APIView):
    def get(self, request, *args, **kwargs):
            profile = Profile.objects.exclude(user=request.user).order_by('?').last()
            return Response(ProfileSerializer(profile, context={'request': request}).data,
                            status=status.HTTP_200_OK)

class ProfileSimilarity(APIView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            username = request.GET.get('username')
            user_profile = request.user.profile
            user_post_songs = user_profile.posts.all()

            # Get audio IDs for the specified username
            username_post_songs = Profile.objects.filter(user__username=username).first().posts.all().values_list(
                'audio_id', flat=True)

            us_p = user_post_songs.filter(audio__id__in=username_post_songs).values('audio_id')
            us_n = user_post_songs.filter(audio__id__in=username_post_songs).values('audio__name')
            # Group user posts by audio and aggregate palettes
            user_palettes = (
               us_n  # Group by audio ID
                .annotate(palettes=Count('palette'))  # You can change this to aggregate palettes
                .annotate(palette_list=F('palette'))  # If you want to keep the palette information
            )

            # Group username posts by audio and aggregate palettes
            username_palettes = (
                Profile.objects.filter(user__username=username)
                .first().posts.filter(audio__id__in=us_p)
                .values('audio__name')  # Group by audio ID
                .annotate(palettes=Count('palette'))  # You can change this to aggregate palettes
                .annotate(palette_list=F('palette'))  # If you want to keep the palette information
            )

            return Response(
                {
                    'user': list(user_palettes),
                    'username': list(username_palettes)
                },
                status=200
            )
        return Response(
            {
                'error':'login'
            },
            status=400
        )


class ProfileFollowView(APIView):
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            username = request.data.get('username')

            if username != request.user.username:
                user_to_follow = User.objects.filter(username=username).last()

                if user_to_follow:
                    user_follow_profile = user_to_follow.profile
                    current_user_profile = request.user.profile

                    if user_follow_profile not in current_user_profile.following.all():

                        current_user_profile.following.add(user_follow_profile)
                        user_follow_profile.follower.add(current_user_profile)

                        status = 'followed'
                    else:
                        # Unfollow the user
                        current_user_profile.following.remove(user_follow_profile)
                        user_follow_profile.follower.remove(current_user_profile)
                        status = 'unfollowed'

                    return Response({'status': status}, status=200)

                # If the user does not exist
                return Response({'error': 'user not found'}, status=404)

            # If trying to follow themselves
            return Response({'error': 'cannot follow yourself'}, status=400)

        # If the user is not authenticated
        return Response({'error': 'not authenticated'}, status=401)




