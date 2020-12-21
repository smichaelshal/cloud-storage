from django.conf.urls import include
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('websocket/', include('websocketApp.urls')),
    path('files/', include('filesApp.urls')),
    path('users/', include('usersApp.urls')),

    path('admin/', admin.site.urls),
]