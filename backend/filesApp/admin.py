from django.contrib import admin
from .models import Profile, File, Directory, Permission, LastAction

admin.site.register(Profile)
admin.site.register(File)
admin.site.register(Directory)
admin.site.register(Permission)
admin.site.register(LastAction)
