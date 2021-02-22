from django.urls import path, include

from .views import (
    UploadFileApi,
    CreatePathApi,
    GetStructDirectry,
    GetListFilesDirectories,
    GetLastUpload,
    GetLastDownload,
    GetListDirectoriesApi,
    ChnageNameObject,
    DeleteObject,
    ShareObject,
    GetIdsUsers
    )


urlpatterns = [
    path('api/uploadfileapi/', UploadFileApi.as_view(), name='uploadfileapi'),
    path('api/createpathapi/', CreatePathApi.as_view(), name='createpathapi'),
    path('api/getstructdirectry/', GetStructDirectry.as_view(), name='getstructdirectry'),
    path('api/getlistfilesdirectories/', GetListFilesDirectories.as_view(), name='getlistfilesdirectories'),
    path('api/getlistdirectories/', GetListDirectoriesApi.as_view(), name='getlistdirectories'),
    path('api/getlastupload/', GetLastUpload.as_view(), name='getlastupload'),
    path('api/getlastdownload/', GetLastDownload.as_view(), name='getlastdownload'),
    path('api/chnagenameobject/', ChnageNameObject.as_view(), name='chnagenameobject'),
    path('api/deleteobject/', DeleteObject.as_view(), name='deleteobject'),
    path('api/shareobject/', ShareObject.as_view(), name='shareobject'),
    path('api/getidsusers/', GetIdsUsers.as_view(), name='getidsusers'),
]

