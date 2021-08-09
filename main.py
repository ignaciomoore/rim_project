import time

import numpy
from scipy.spatial import distance

from duplicate_searcher import Candidate

if __name__ == "__main__":
    debra_song_descriptors_file = "C:/Users/iggym/Documents/Recuperacion de Informacion Multimedia/rim_project/debra_song_descriptors.bin"
    song_descriptors_file = debra_song_descriptors_file  # <- change here

    movie_audio_descriptors_file = "C:/Users/iggym/Documents/Recuperacion de Informacion Multimedia/rim_project/baby_driver_audio_descriptors.bin"
    debra_song_shape = (3434, 32)

    song_shape = debra_song_shape  # <- change here

    movie_audio_shape = (67598, 32)

    t2 = time.time()
    song_descriptors = numpy.fromfile(song_descriptors_file, sep="\n").reshape(song_shape)
    movie_audio_descriptors = numpy.fromfile(movie_audio_descriptors_file, sep="\n").reshape(movie_audio_shape)
    t3 = time.time()

    print(f"Reading {round(t3 - t2, 2)} secs")

    t0 = time.time()
    distances = distance.cdist(song_descriptors, movie_audio_descriptors)
    t1 = time.time()
