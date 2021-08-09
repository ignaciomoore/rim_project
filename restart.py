
import os
import subprocess
import librosa
import numpy
import time
from scipy.spatial import distance

def extract_audio(video_file, sample_rate, audio_folder):
    file = "{}.{}.wav".format(audio_folder, sample_rate)
    print(file)
    if os.path.isfile(file):
        return file
    comando = ["ffmpeg", "-i", video_file, "-ac", "1", "-ar", str(sample_rate), file]
    print("STARTING: {}".format(" ".join(comando)))
    code = subprocess.call(comando, shell=True)
    if code != 0:
        raise Exception("ERROR!")
    return file


def create_audio_descriptors(audio_file, sample_rate, dimension, window, hop):
    y, sr = librosa.load(audio_file, sample_rate)
    mfcc = librosa.feature.mfcc(y, sr=sr, n_mfcc=dimension, n_fft=window, hop_length=hop)
    return mfcc.transpose()


if __name__ == "__main__":
    debra_video = "C:/Users/iggym/Documents/Movies/Baby Driver (2017) [YTS.AG]/Soundtrack/[ONTIVA.COM] Debra-144p.mp4"
    test_audio = "debra audio test"
    new_test_audio = "debra audio test.22000.wav"
    # extract_audio(debra_video, 22000, test_audio)
    descriptors_file = "new debra song descriptors.bin"
    movie_descriptors_file = "baby_driver_audio_descriptors.bin"
    """
    descriptors = create_audio_descriptors(new_test_audio, 22000, 32, 2200, 2200)
    print(descriptors.shape)
    
    descriptors.tofile(descriptors_file, sep="\n")
    """
    song_shape = (3434, 32)

    song_descriptors = numpy.fromfile(descriptors_file, sep="\n").reshape(song_shape)
    print(song_descriptors.shape)

    movie_shape = (67598, 32)
    movie_descriptors = numpy.fromfile(movie_descriptors_file, sep="\n").reshape(movie_shape)
    print(movie_descriptors.shape)

    t0 = time.time()
    distances = distance.cdist(song_descriptors, movie_descriptors)
    t1 = time.time()

    print(f"Distances {distances.shape} {round(t1-t0, 2)} secs")

    number_of_neighbours = 5

    neighbours = []
    t10 = time.time()
    for song_descriptor in distances:
        neighbours.append(numpy.argpartition(song_descriptors, number_of_neighbours)[:number_of_neighbours])
    t11 = time.time()
    neighbours = numpy.array(neighbours)
    print(f"Neighbours {neighbours.shape} {round(t11-t10, 2)} secs")

