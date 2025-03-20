from django.urls import path

from file_uploader.consumers import UploadJobConsumer

websocket_urlpatterns = [
    path("ws/upload/<str:channel_name>/", UploadJobConsumer.as_asgi()),
]
