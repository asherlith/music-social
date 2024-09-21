from django.urls import path
from .views import LoginView, RegisterView, ResetPasswordView, ProfileUsernameView, RegisterVerifyView, ProfileView, \
    ProfileSearchView, ProfileStatisticsView, ProfileSearchRandomView, ProfileSimilarity, ProfileFollowView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),

    path('register/', RegisterView.as_view(), name='register'),
    path('register/verify/', RegisterVerifyView.as_view(), name='login'),

    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/statistics/', ProfileStatisticsView.as_view(), name='profile'),

    path('profile/search/', ProfileSearchView.as_view(), name='search'),
    path('profile/similarity/', ProfileSimilarity.as_view(), name='search'),

    path('profile/search/random/', ProfileSearchRandomView.as_view(), name='search'),
    path('profile/follow/', ProfileFollowView.as_view(), name='search'),

    path('profile/user/<str:username>/', ProfileUsernameView.as_view(), name='profile'),


    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),

]
