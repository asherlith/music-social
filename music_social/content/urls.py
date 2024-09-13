from django.urls import path
from .views import SongsView


urlpatterns = [
    path('songs/', SongsView.as_view(), name='login'),
]