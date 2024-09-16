import librosa
import numpy as np
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

def handle_graph(energy, colors, y, sr, file_name='waveform_with_colors.png'):
    # Convert energy to a numpy array and reshape
    features = np.array(energy).reshape(-1, 1)

    # KMeans clustering
    kmeans = KMeans(n_clusters=5)
    kmeans.fit(features)

    # Predict and assign colors to clusters
    labels = kmeans.labels_
    color_labels = dict(zip(np.unique(labels), colors))

    # Plot the waveform
    plt.figure(figsize=(10, 6))
    librosa.display.waveshow(y, sr=sr)

    # Add color annotations to the waveform
    for time_interval, label in color_labels.items():
        plt.axvline(x=time_interval, color=label, linestyle='--')

    # Set plot titles and labels
    plt.title('Waveform with K-means Color Annotations')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')

    # Save the figure
    plt.savefig(file_name)  # Save the plot as an image file
    plt.show()  # Optionally, display the plot as well

    print(f"Plot saved as {file_name}")
