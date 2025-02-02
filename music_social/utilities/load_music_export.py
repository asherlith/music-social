import sys

import eyed3
from os import listdir, environ, getcwd
import django
import librosa
from django.core.files import File


def initial():
    sys.path.append("..")
    environ["DJANGO_SETTINGS_MODULE"] = "music_social.settings"
    django.setup()


initial()

from content.models import Artist, Album, Song

import librosa

def extract_features(y, sr, frame_length=2048, hop_length=512):
    energy = librosa.feature.rms(y=y, frame_length=frame_length, hop_length=hop_length)
    times = librosa.times_like(energy, sr=sr, hop_length=hop_length)
    return times, energy.flatten()



for file in listdir('../files'):
    print(f"INSERTING FILE {file}")
    try:
        path = '../files/' + file

        if file.lower().endswith('mp3'):
          audio = eyed3.load(path)

          if not Album.objects.filter(name=audio.tag.album).exists():
               album = Album.objects.create(name=audio.tag.album)
          else:
               album = Album.objects.filter(name=audio.tag.album).last()


          if not Artist.objects.filter(name=audio.tag.artist).exists():
               artist = Artist.objects.create(name=audio.tag.artist)
          else:
               artist = Artist.objects.filter(name=audio.tag.artist).last()


          if not Song.objects.filter(name=audio.tag.title, artist=artist, album=album).exists():
               song = Song.objects.create(
                   name=audio.tag.title,
                   artist=artist,
                   album=album,
               )

          else:
              song = Song.objects.filter(name=audio.tag.title, artist=artist, album=album).last()

          if not song.audio:
              with open(path, 'rb') as f:
                  django_file = File(f)
                  song.audio = django_file
                  song.save()

          if song.duration==0:
              song.duration = audio.info.time_secs
              song.save()

          y, sr = librosa.load(path)

          times, energy = extract_features(y, sr)
          song.times = times.tolist()
          song.energy = energy.tolist()
          song.save()

    except Exception as e:
        print(e)


for file in listdir('../files'):
    print(f"INSERTING FILE {file}")
    try:
        path = '../files/' + file

        if file.lower().endswith('jpg'):
            name = file.lower().replace('.mp3_thumb.jpg', '')
            song = Song.objects.filter(name__icontains=name).last()

            if song and name == song.name.lower() and not song.cover:
                with open(path, 'rb') as f:
                    django_file = File(f)
                    song.cover = django_file
                    song.save()

    except Exception as e:
        print(e)
