from django.db import models
from django.contrib.auth.models import User

class Permission(models.Model):
    permission_to_share = models.ManyToManyField(User, related_name = 'share', symmetrical=False)
    permission_to_download = models.ManyToManyField(User, related_name = 'download', symmetrical=False)
    permission_to_read = models.ManyToManyField(User, related_name = 'read', symmetrical=False)
    permission_to_view = models.ManyToManyField(User, related_name = 'view', symmetrical=False)

class File(models.Model):
    name_file = models.CharField(max_length=50, default='FILE')
    type_file = models.CharField(max_length=5, default='txt')
    id_file = models.CharField(max_length=128, default=0)
    size_file = models.PositiveIntegerField(default=0)
    user_upload = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    seek_file = models.PositiveIntegerField(default=0)

    pathDestination = models.CharField(max_length=256, default='/')
    pathSource = models.CharField(max_length=256, default='/')

    permission_file = models.ForeignKey(Permission, on_delete=models.CASCADE, null=True, blank=True)

    created_date = models.DateField(null=True, blank=True)
    changed_date = models.DateField(null=True, blank=True)
    upload_date = models.DateField(null=True, blank=True)
    download_date = models.DateField(null=True, blank=True)

class Directory(models.Model):
    name_directory = models.CharField(max_length=50, null=True, blank=True)
    size_directory = models.PositiveIntegerField(null=True, blank=True)
    user_upload = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    id_directory = models.CharField(max_length=128, default=0)

    files = models.ManyToManyField(File, related_name = 'files', symmetrical=False)
    directories = models.ManyToManyField('self', related_name = 'directoriesList', symmetrical=False)

    permission_directory = models.ForeignKey(Permission, on_delete=models.CASCADE, null=True, blank=True)

    created_date = models.DateField(null=True, blank=True)
    changed_date = models.DateField(null=True, blank=True)
    upload_date = models.DateField(null=True, blank=True)
    download_date = models.DateField(null=True, blank=True)

    pathDestination = models.CharField(max_length=256, default='/')
    pathSource = models.CharField(max_length=256, default='/')

class LastAction(models.Model):
    LAST_ACTION = [
        ('up', 'upload'),
        ('down', 'download')
    ]

    name_action = models.CharField(max_length=4, choices=LAST_ACTION, default='up')
    object_active = models.ForeignKey(File, on_delete=models.CASCADE, null=True, blank=True)
    is_end_action = models.BooleanField(default=True)
    counter = models.PositiveIntegerField(default=0)
    date_action = models.DateField(null=True, blank=True)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True, blank=True)
    is_active = models.BooleanField(default=False)
    root_directory = models.ForeignKey(Directory, on_delete=models.CASCADE, null=True, blank=True, related_name = 'root_directory')
    last_upload = models.ForeignKey(LastAction, on_delete=models.CASCADE, related_name = 'last_upload', null=True, blank=True)
    last_download = models.ForeignKey(LastAction, on_delete=models.CASCADE, related_name = 'last_download', null=True, blank=True)
    
    deleted_directory = models.ForeignKey(Directory, on_delete=models.CASCADE, null=True, blank=True, related_name = 'deleted_directory')