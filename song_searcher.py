
import sys
import numpy
from scipy.spatial import distance
import time
import datetime

# song_descriptors_file = "opening_song_descriptors.bin"
song_descriptors_file = sys.argv[1]
# movie_audio_descriptors_file = "baby_driver_audio_descriptors.bin"
movie_audio_descriptors_file = sys.argv[3]

# opening_song_shape = (3416, 32)
# movie_audio_shape = (72780, 32)
song_shape = (int(sys.argv[2]), 32)
movie_audio_shape = (int(sys.argv[4]), 32)

t2 = time.time()
song_descriptors = numpy.fromfile(song_descriptors_file, sep="\n").reshape(song_shape)
movie_audio_descriptors = numpy.fromfile(movie_audio_descriptors_file, sep="\n").reshape(movie_audio_shape)
t3 = time.time()

print(f"Reading {t3-t2}")

t0 = time.time()
distances = distance.cdist(song_descriptors, movie_audio_descriptors)
t1 = time.time()

print(f"Distances {distances.shape} {t1-t0}")


def get_k_smallest_distance(k, distances, min_dist, current_k):
    if current_k == k:
        return distances[distances > min_dist].min()
    new_min_dist = distances[distances > min_dist].min()
    return numpy.append(new_min_dist, get_k_smallest_distance(k, distances, new_min_dist, current_k + 1))

"""
t5 = time.time()
minimum_distance = numpy.amin(distances)
# minimum_distance = get_k_smallest_distance(1, distances)
t6 = time.time()
location = numpy.where(distances == numpy.amin(distances))
t7 = time.time()

"""
def audio_second(sample_rate, window, descriptor_index):  # if hop == window
    return str(datetime.timedelta(seconds=round((1/sample_rate)*window*descriptor_index)))

"""
listOfCordinates = list(zip(location[0], location[1]))

print(f"Minimum distance {minimum_distance} {t6-t5}")
print(f"Locations {t7-t6}")


for cord in listOfCordinates:
    print(f"{cord} | {audio_second(44100, 4096, cord[0])} song sec | {audio_second(44100, 4096, cord[1])} movie sec") 

min_2_dist = distances[distances > minimum_distance].min()
loc_2 = numpy.where(distances == min_2_dist)
print(f"Dist = {min_2_dist}, loc = {loc_2}")
"""

k = 50

t10 = time.time()
min_k_dists = get_k_smallest_distance(k, distances, 0, 1)
t11 = time.time()

print(f"Min {k} distances = {min_k_dists} | {round(t11-t10)} secs")

locations = []
for min_dist in min_k_dists:
    locations.append(numpy.where(distances == min_dist))

i = 0
for location in locations:
    i += 1
    listOfCordinates = list(zip(location[0], location[1]))
    print(f"Values for min {i} distance")
    for cord in listOfCordinates:
        print(f"    {cord} | {audio_second(44100, 4096, cord[0])} song sec | {audio_second(44100, 4096, cord[1])} movie sec")

