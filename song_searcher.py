
import sys
import numpy
from scipy.spatial import distance
import time
import datetime
import matplotlib.pyplot as plt


opening_song_file = "opening_song_descriptors.bin"
debra_song_file = "debra_song_descriptors.bin"
song_descriptors_file = opening_song_file

movie_audio_descriptors_file = "baby_driver_audio_descriptors.bin"


opening_song_shape = (3416, 32)
debra_song_shape = ()

song_shape = opening_song_shape
movie_audio_shape = (72780, 32)

"""
song_descriptors_file = sys.argv[1]
movie_audio_descriptors_file = sys.argv[3]

song_shape = (int(sys.argv[2]), 32)
movie_audio_shape = (int(sys.argv[4]), 32)
"""

t2 = time.time()
song_descriptors = numpy.fromfile(song_descriptors_file, sep="\n").reshape(song_shape)
movie_audio_descriptors = numpy.fromfile(movie_audio_descriptors_file, sep="\n").reshape(movie_audio_shape)
t3 = time.time()

print(f"Reading {round(t3-t2, 2)} secs")

t0 = time.time()
distances = distance.cdist(song_descriptors, movie_audio_descriptors)
t1 = time.time()

print(f"Distances {distances.shape} {round(t1-t0, 2)} secs")


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


def descriptor_seconds(second_duration, sample_rate, window):
    return round(second_duration * sample_rate / window)


def get_min_dist(distances, threshold, iprint=True):
    t0 = time.time()
    min_dist = distances[distances > threshold].min()
    location = numpy.where(distances == min_dist)
    listOfCordinates = list(zip(location[0], location[1]))
    t1 = time.time()
    if iprint:
        print(f"Min dist {min_dist} {round(t1-t0, 2)} secs")
        for cord in listOfCordinates:
            print(f"{cord} | {audio_second(44100, 4096, cord[0])} song sec | {audio_second(44100, 4096, cord[1])} movie sec")
    return min_dist, listOfCordinates


def get_neigh_dists(coords, distances, min_dist, num_neighs, iprint=True):
    t0 = time.time()
    neigh_dists = []
    neigh_coords_list = [coords]
    for i in range(num_neighs)[1:]:
        if coords[0]+i == distances.shape[0] or coords[1]+i == distances.shape[1]:
            print("Not enough space for more neigbours")
            break
        neigh_dists.append(distances[coords[0]+i][coords[1]+i])
        neigh_coords_list.append((coords[0]+i, coords[1]+i))
    neigh_dists = numpy.array(neigh_dists)
    max_dist_dif = max(abs(min_dist-neigh_dists.min()), abs(min_dist-neigh_dists.max()))
    t1 = time.time()
    if iprint:
        print(f"Max diff {round(max_dist_dif, 2)} | {round(t1-t0, 2)} secs")
    return max_dist_dif, neigh_coords_list

def get_min_dist_seq(distances, min_dist, seq_len, max_acc_dif, iteration, iprint=True): #
    t0 = time.time()
    new_min_dist, listOfCordinates = get_min_dist(distances, min_dist, iprint=False)
    max_dist_dif, neigh_coords_list = get_neigh_dists(listOfCordinates[0], distances, new_min_dist, seq_len, iprint=False)
    t1 = time.time()
    if max_dist_dif <= max_acc_dif and len(neigh_coords_list) == seq_len:
        return new_min_dist, neigh_coords_list, iteration
    print(f"Seq attempt number {iteration}", end="\r")
    min_dist, neigh_coords_list, attempts = get_min_dist_seq(distances, new_min_dist, seq_len, max_acc_dif, iteration+1) #
    return min_dist, neigh_coords_list, attempts


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
threshold = 0
seconds = 5
seq_len = descriptor_seconds(seconds, 44100, 4096)
print(seq_len)
acc_max_dif = 250

min_dist, neigh_coords_list, attempts = get_min_dist_seq(distances, threshold, seq_len, acc_max_dif, 1)
print(f"Min Dist {min_dist} | Num Attempts {attempts}")
for cord in neigh_coords_list:
        print(f"{cord} | {audio_second(44100, 4096, cord[0])} song sec | {audio_second(44100, 4096, cord[1])} movie sec")

"""
t20 = time.time()
distances_array = distances.flatten()
t21 = time.time()
print(f"Flatten {round(t21-t20, 2)} secs")
print(distances_array.shape)
# numpy.histogram(distances)

plt.hist(distances_array, bins='auto')  # arguments are passed to np.histogram
plt.title("Histogram with 'auto' bins")
plt.show()
"""
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
"""
