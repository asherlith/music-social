import ast
import io
import json

import numpy as np
from django.core.files.base import ContentFile
from matplotlib import pyplot as plt, patches

from user_content.models import ProfilePost
from utilities.path import profile_colors_path


def get_user_color_stats(user_id):
    posts = ProfilePost.objects.filter(profile__user=user_id)
    song_color_map = {}

    for post in posts:
        song_id = post.audio
        tuple_list = ast.literal_eval(post.palette)
        colors = [list(tup) for tup in tuple_list]

        if song_id not in song_color_map:
            song_color_map[song_id] = {'color_count': {}, 'total_posts': 0}

        song_color_map[song_id]['total_posts'] += 1

        for color in colors:
            color_key = ','.join(map(str, color))
            if color_key not in song_color_map[song_id]['color_count']:
                song_color_map[song_id]['color_count'][color_key] = 0
            song_color_map[song_id]['color_count'][color_key] += 1
    return song_color_map


def generate_statistics(user_id):
    song_color_map = get_user_color_stats(user_id)

    statistics = {}
    for song_id, data in song_color_map.items():
        total_posts = data['total_posts']
        color_stats = {color: count / total_posts for color, count in data['color_count'].items()}
        statistics[f'{song_id}'] = {
            'total_posts': total_posts,
            'color_statistics': color_stats
        }
    return statistics

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)


def calculate_median_color(color_stats):
    """Calculate the median color from a dictionary of color frequencies."""
    rgb_values = []
    for color, value in color_stats.items():
        rgb = tuple(map(int, color.split(',')))
        # Add the RGB value to the list multiplied by its frequency weight
        rgb_values.extend([rgb] * int(value * 100))  # Scaling by 100 to avoid float issues

    # Convert the list to a numpy array for easier median calculation
    rgb_values = np.array(rgb_values)

    # Calculate the median of each RGB channel
    median_rgb = np.median(rgb_values, axis=0).astype(int)

    return tuple(median_rgb)

def plot_color_distribution(data, instance, field_name='image_field'):
    """Plot the median color for each song and save the image to a Django model's ImageField."""
    songs = list(data.keys())
    medians = []

    # Calculate the median color for each song
    for song in songs:
        color_stats = data[song]['color_statistics']
        median_color = calculate_median_color(color_stats)
        medians.append(median_color)

    # Create a figure for plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the median colors
    for idx, song in enumerate(songs):
        median_color = medians[idx]
        hex_color = rgb_to_hex(median_color)
        ax.add_patch(patches.Rectangle((idx, 0), 1, 1, color=hex_color))
        ax.text(idx + 0.5, -0.2, song, ha='center', rotation=45, fontsize=10)

    # Customize the axis
    ax.set_xlim(0, len(songs))
    ax.set_ylim(-1, 1)
    ax.set_xticks([])
    ax.set_yticks([])

    plt.title('Median Color of Each Song')

    # Save the plot to a BytesIO object (in-memory file)
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', dpi=300)
    plt.close(fig)

    # Save the image to the model's ImageField
    buffer.seek(0)  # Reset buffer pointer to the beginning
    image_name = 'median_colors_plot.png'

    # Set the ImageField value (assuming your ImageField is named 'image_field')
    getattr(instance, field_name).save(image_name, ContentFile(buffer.read()), save=False)

    # Optionally, save the instance to store the image in the database
    instance.save()