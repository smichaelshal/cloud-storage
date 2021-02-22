from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/upload/', consumers.UploadConsumer.as_asgi()),
    re_path(r'ws/download/', consumers.DownloadConsumer.as_asgi()),
    re_path(r'ws/message/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
]