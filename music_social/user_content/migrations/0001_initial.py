# Generated by Django 4.2.1 on 2024-09-16 02:22

from django.db import migrations, models
import django.db.models.deletion
import utilities.path


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileSong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('biography_song_start_second', models.IntegerField()),
                ('biography_song_end_second', models.IntegerField()),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_song', to='user.profile')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='content_profile_song', to='content.song')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProfilePost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('modified_time', models.DateTimeField(auto_now=True)),
                ('file', models.FileField(upload_to=utilities.path.profile_post_path)),
                ('audio_start', models.FloatField(default=0)),
                ('audio_end', models.FloatField(default=0)),
                ('caption', models.TextField(blank=True)),
                ('is_archive', models.BooleanField(default=False)),
                ('is_daily', models.BooleanField(default=False)),
                ('is_main', models.BooleanField(default=False)),
                ('is_color', models.BooleanField(default=False)),
                ('audio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='content.song')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='user.profile')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
