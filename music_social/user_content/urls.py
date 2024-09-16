from django.urls import path
from .views import UploadContentView, GetContentView


urlpatterns = [
    path('post/', UploadContentView.as_view(), name='post'),
    path('get_post/', GetContentView.as_view(), name='post'),

]