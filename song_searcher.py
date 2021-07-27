
import numpy
from scipy.spatial import distance
import time

song_descriptors_file = "opening_song_descriptors.bin"
movie_audio_descriptors_file = "baby_driver_audio_descriptors.bin"

opening_song_shape = (3416, 32)
movie_audio_shape = (72780, 32)

t2 = time.time()
song_descriptors = numpy.fromfile(song_descriptors_file, sep="\n").reshape(opening_song_shape)
movie_audio_descriptors = numpy.fromfile(movie_audio_descriptors_file, sep="\n").reshape(movie_audio_shape)
t3 = time.time()

print(f"Reading {t3-t2}")

t0 = time.time()
distances = distance.cdist(song_descriptors, movie_audio_descriptors)
t1 = time.time()

print(f"Distances {distances.shape} {t1-t0}")

t5 = time.time()
minimum_distance = numpy.amin(distances)
t6 = time.time()
location = numpy.where(distances == numpy.amin(distances))
t7 = time.time()

print(f"Minimum distance {minimum_distance} {t6-t5}")
print(f"Location count {location[0].shape} {t7-t6}")

