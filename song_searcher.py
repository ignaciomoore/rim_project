
import sys
import numpy
from scipy.spatial import distance
import time
import datetime
import matplotlib.pyplot as plt


def get_k_smallest_distance(k, distances, min_dist, current_k):
    if current_k == k:
        return distances[distances > min_dist].min()
    new_min_dist = distances[distances > min_dist].min()
    return numpy.append(new_min_dist, get_k_smallest_distance(k, distances, new_min_dist, current_k + 1))


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
            print("Not enough space for more neighbours")
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
    min_dist, neigh_coords_list, attempts = get_min_dist_seq(distances, new_min_dist, seq_len, max_acc_dif, iteration+1)
    return min_dist, neigh_coords_list, attempts


def add_offset_to_index(offset_threshold, index, offset):
    if index >= offset_threshold:
        return index + (offset*2)
    return index


def get_closest_neighbours(song_index, num_of_neighs, distance_matrix, min_offset):
    offset_range = ((song_index - min_offset) % distance_matrix.shape[1], (song_index + min_offset) % distance_matrix.shape[1])
    switch = True
    
    if offset_range[0] < offset_range[1]:
        start_neighs = distance_matrix[song_index][:offset_range[0]]
        end_neighs = distance_matrix[song_index][offset_range[1]:]
        new_neighs = numpy.append(start_neighs, end_neighs)
    else:
        new_neighs = distance_matrix[song_index][offset_range[1]:offset_range[0]]

    results = numpy.argpartition(new_neighs, num_of_neighs)[:num_of_neighs]
    new_results = []
    for i in range(len(results)):
        if switch:
            offset_threshold = offset_range[1]
            new_results.append(add_offset_to_index(offset_threshold, results[i], min_offset))
        else:
            offset_threshold = offset_range[0]
            new_results.append(add_offset_to_index(offset_threshold, results[i], min_offset))

    return numpy.array(new_results)

import subprocess

def play_result(video_file, results,  descriptors_per_second, index=0):
    index = int(input("Please enter match index: "))
    cand = results[index]
    song_init_tmstmp = str(datetime.timedelta(seconds=int(cand.song_descriptor_index / descriptors_per_second)))
    duration = str(datetime.timedelta(seconds=int(cand.sequence_duration / descriptors_per_second)))
    movie_init_tmstmp = str(datetime.timedelta(seconds=int(cand.movie_descriptor_index / descriptors_per_second)))

    command = ["ffplay", "-ss", song_init_tmstmp, "-i", video_file, "-t", duration]
    code = subprocess.call(command, shell=True)
    if code != 0:
        raise Exception("ERROR!")

    command = ["ffplay", "-ss", movie_init_tmstmp, "-i", video_file, "-t", duration]
    code = subprocess.call(command, shell=True)
    if code != 0:
        raise Exception("ERROR!")

