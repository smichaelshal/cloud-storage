# Generated by Django 3.1.3 on 2020-12-11 08:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('filesApp', '0006_auto_20201211_0810'),
    ]

    operations = [
        migrations.AddField(
            model_name='directory',
            name='changed_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='directory',
            name='created_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='directory',
            name='directories',
            field=models.ManyToManyField(related_name='directoriess', to='filesApp.Directory'),
        ),
        migrations.AddField(
            model_name='directory',
            name='download_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='directory',
            name='files',
            field=models.ManyToManyField(related_name='files', to='filesApp.File'),
        ),
        migrations.AddField(
            model_name='directory',
            name='name_directory',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='directory',
            name='pathDestination',
            field=models.CharField(default='/', max_length=256),
        ),
        migrations.AddField(
            model_name='directory',
            name='pathSource',
            field=models.CharField(default='/', max_length=256),
        ),
        migrations.AddField(
            model_name='directory',
            name='permission_directory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='filesApp.permission'),
        ),
        migrations.AddField(
            model_name='directory',
            name='size_directory',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='directory',
            name='upload_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='directory',
            name='user_upload',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='file',
            name='changed_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='created_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='download_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='id_file',
            field=models.CharField(default=0, max_length=128),
        ),
        migrations.AddField(
            model_name='file',
            name='name_file',
            field=models.CharField(default='FILE', max_length=50),
        ),
        migrations.AddField(
            model_name='file',
            name='pathDestination',
            field=models.CharField(default='/', max_length=256),
        ),
        migrations.AddField(
            model_name='file',
            name='pathSource',
            field=models.CharField(default='/', max_length=256),
        ),
        migrations.AddField(
            model_name='file',
            name='permission_file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='filesApp.permission'),
        ),
        migrations.AddField(
            model_name='file',
            name='seek_file',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='file',
            name='size_file',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='file',
            name='type_file',
            field=models.CharField(default='txt', max_length=5),
        ),
        migrations.AddField(
            model_name='file',
            name='upload_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='file',
            name='user_upload',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lastaction',
            name='counter',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='lastaction',
            name='date_action',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lastaction',
            name='is_end_action',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='lastaction',
            name='name_action',
            field=models.CharField(choices=[('up', 'upload'), ('down', 'download')], default='up', max_length=4),
        ),
        migrations.AddField(
            model_name='lastaction',
            name='object_active',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='filesApp.file'),
        ),
        migrations.AddField(
            model_name='permission',
            name='permission_to_download',
            field=models.ManyToManyField(related_name='download', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='permission',
            name='permission_to_read',
            field=models.ManyToManyField(related_name='read', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='permission',
            name='permission_to_share',
            field=models.ManyToManyField(related_name='share', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='permission',
            name='permission_to_view',
            field=models.ManyToManyField(related_name='view', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_download',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_download', to='filesApp.lastaction'),
        ),
        migrations.AddField(
            model_name='profile',
            name='last_upload',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='last_upload', to='filesApp.lastaction'),
        ),
        migrations.AddField(
            model_name='profile',
            name='root_directory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='filesApp.directory'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
