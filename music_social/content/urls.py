from django.urls import path
from .views import SongsView, SongsDetailView

urlpatterns = [
    path('songs/', SongsView.as_view(), name='login'),
    path('songs/<int:id>/', SongsDetailView.as_view(), name='login'),

]