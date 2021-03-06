# Generated by Django 3.1.3 on 2021-01-29 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('filesApp', '0009_directory_id_directory'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='deleted_directory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deleted_directory', to='filesApp.directory'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='root_directory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='root_directory', to='filesApp.directory'),
        ),
    ]
