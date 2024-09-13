# Generated by Django 4.2.1 on 2024-09-12 15:25

from django.db import migrations, models
import utilities.path


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to=utilities.path.audio_path),
        ),
        migrations.AddField(
            model_name='song',
            name='cover',
            field=models.ImageField(blank=True, null=True, upload_to=utilities.path.audio_cover_path),
        ),
    ]
