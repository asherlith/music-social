from django.urls import path
from .views import LoginView, RegisterView, ResetPasswordView, RegisterVerifyView, ProfileView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),

    path('register/', RegisterView.as_view(), name='register'),
    path('register/verify/', RegisterVerifyView.as_view(), name='login'),

    path('profile/', ProfileView.as_view(), name='profile'),

    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),

]
