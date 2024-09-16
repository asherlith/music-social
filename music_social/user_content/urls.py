from django.urls import path

from .views import UploadContentView, GetContentView, DeleteContentView


urlpatterns = [
    path('post/', UploadContentView.as_view(), name='post'),
    path('post/<int:id>/', DeleteContentView.as_view(), name='post'),

    path('get_post/', GetContentView.as_view(), name='post'),

]