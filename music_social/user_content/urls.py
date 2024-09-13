from django.urls import path
from .views import UploadContentView


urlpatterns = [
    path('post/', UploadContentView.as_view(), name='post'),
]