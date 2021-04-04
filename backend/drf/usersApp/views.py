#django
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

#rest_framework
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated   
from rest_framework import generics
from rest_framework import serializers
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

#serializers
from .serializers import ChangePasswordSerializer
from .serializers import UserSerializer, RegisterSerializer

#models
from django.contrib.auth.models import User
from filesApp.models import Directory, Profile, LastAction, File, Permission

import secrets


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    """
    post login,
    params: request,
    return Response http 200 OK
    """
    username = request.data.get("username")
    password = request.data.get("password")
    if (username is None or password is None) or (username == "admin"):
        return Response({'msg': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'msg': 'Username or password is incorrect.'},
                        status=HTTP_400_BAD_REQUEST)
    
    listToken = Token.objects.all().filter(user=user)
    if len(listToken) != 0:
        return Response({'msg': 'The user is already logged in.'},
                        status=HTTP_400_BAD_REQUEST)

    token, _ = Token.objects.get_or_create(user=user)

    profileUser = user.profile
    profileUser.is_active = True
    profileUser.save()
    idUser = str(user.id)
    
    return Response({'token': token.key, 'id': idUser},
                    status=HTTP_200_OK)

class RegisterAPI(generics.GenericAPIView):
    """
    class of User registration.
    """
    serializer_class = RegisterSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
            User registration
            params: request,
            return response HTTP 200 OK
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        password = request.data['password']
        # password2 = request.data['password2']
        # if password != password2:
        #     raise serializers.ValidationError({'msg':'Passowrd must match.'})

        user = serializer.save()

        newFile = File(name_file='First File', type_file='txt', id_file='0', user_upload=user, size_file=0, seek_file=0, pathDestination='/', pathSource='/')
        newFile.save()

        root_directory = Directory(name_directory='/', size_directory=0, user_upload=user, pathDestination='/', pathSource='/', id_directory=secrets.token_hex(16))
        root_directory.save()

        deleted_directory = Directory(name_directory='deleted', size_directory=0, user_upload=user, pathDestination='/', pathSource='/', id_directory=secrets.token_hex(16))
        deleted_directory.save()

        newProfile = Profile(user=user, is_active=False, root_directory=root_directory, deleted_directory=deleted_directory)
        newProfile.save()

        permissionsFile = Permission()
        permissionsFile.save()
        permissionsFile.permission_to_share.add(user)
        permissionsFile.permission_to_download.add(user)
        permissionsFile.permission_to_read.add(user)
        permissionsFile.permission_to_view.add(user)
        permissionsFile.save()

        newProfile.permission_file = permissionsFile
        newProfile.save()

        return Response({"msg": "You have successfully registered"})

class LogoutAPI(generics.GenericAPIView):
    """
        class of User logout.
    """
    def post(self, request, *args, **kwargs):
        """
            User logout
            params: request,
            return response HTTP 200 OK
        """
        strTokenUser = request.headers["Authorization"].split(' ')[1]
        user = Token.objects.all().filter(key=strTokenUser)[0].user
        user.auth_token.delete()

        profileUser = user.profile
        profileUser.is_active = False
        profileUser.save()

        return Response({"msg": "User logged in successfully."})


class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    
    serializer_class = ChangePasswordSerializer
    model = User
    # permission_classes = (IsAuthenticated,)


    def update(self, request, *args, **kwargs):
        """
            User change password
            params: request,
            return response HTTP 200 OK
        """
        strTokenUser = request.headers["Authorization"].split(' ')[1]
        user = Token.objects.all().filter(key=strTokenUser)[0].user
        self.object = user
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }
            return Response(response)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)