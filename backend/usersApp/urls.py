from django.urls import path, include
from .views import RegisterAPI, LogoutAPI, ChangePasswordView, login

urlpatterns = [
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', login),
    path('api/logout/', LogoutAPI.as_view(), name='logout'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]