# Generated by Django 3.1.3 on 2020-12-03 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filesApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_active',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_action',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='root_directory',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
    ]
