import time

import numpy
from scipy.spatial import distance

from duplicate_searcher import Candidate



if __name__ == "__main__":

    """ CALCULATE DISTANCES """

    descriptors_per_second = 2
    song_shape = (687, 32)
    movie_shape = (13520, 32)

    baby_driver_descriptors_file = f"baby_driver_audio_descriptors_{descriptors_per_second}.bin"
    # debra_song_descriptors_file = "debra_song_descriptors.bin"
    debra_song_descriptors_file = f"debra_song_descriptors_{descriptors_per_second}.bin"

    debra_song_shape = song_shape

    song_descriptors = numpy.fromfile(debra_song_descriptors_file, sep="\n").reshape(debra_song_shape)
    print(song_descriptors.shape)

    movie_shape = movie_shape
    movie_descriptors = numpy.fromfile(baby_driver_descriptors_file, sep="\n").reshape(movie_shape)
    print(movie_descriptors.shape)

    t0 = time.time()
    # distances = distance.cdist(song_descriptors, movie_descriptors)
    distances = distance.cdist(movie_descriptors, movie_descriptors)
    t1 = time.time()

    print(f"Distances {distances.shape} {round(t1-t0, 2)} secs")

    """ GET NEIGHBOURS """

    from duplicate_searcher import Neighbours

    number_of_neighbours = 5

    neighbour_file = "neighbours.txt"
    neighbours = []
    total = distances.shape[0]
    t10 = time.time()
    for i in range(distances.shape[0]):
        print(f"Progress: {round((i/total)*100, 2)}%", end="\r")
        song_descriptor = distances[i]
        neighs = numpy.argpartition(song_descriptor, number_of_neighbours)[:number_of_neighbours]
        neighbours.append(neighs)
    t11 = time.time()
    neighbours = Neighbours(numpy.array(neighbours))
    print(f"Neighbours {neighbours.shape()} {round(t11-t10, 2)} secs")

    """ CREATE CANDIDATES """

    candidates = []
    song_indexes = range(distances.shape[0])
    total_songs = distances.shape[0]
    for song in song_indexes:
        print(f"Progress {round((song/total_songs)*100, 2)}%", end="\r")
        for neighbour in neighbours.search(song):
            candidates.append(Candidate(song, neighbour, descriptors_per_second))

    print(f" Candidates {len(candidates)}")

    """ FIND SEQUENCE """

    copies = []

    max_missing_streak_secs = 1
    max_missing_streak = max_missing_streak_secs * descriptors_per_second
    min_duration_seconds = 3
    min_duration = min_duration_seconds * descriptors_per_second

    total_candidates = len(candidates)
    for i in range(len(candidates)):
        print(f"Progress {round((i/total_candidates)*100, 2)}%", end="\r")
        cand = candidates[i]
        current_candidate = cand.find_next(neighbours, max_missing_streak)
        if current_candidate.sequence_duration >= min_duration and current_candidate.score() >= 1:
            copies.append(current_candidate)

    print(len(copies)) 

    """ CONTAIN """

    filtered = []

    for i in range(len(copies)):
        print(f"Progress {round((i/len(copies))*100, 2)}%", end="\r")
        cani = copies[i]
        add = True
        for j in range(len(copies)):
            canj = copies[j]
            
            if i == j:
                continue
            
            elif cani.contains(canj):
                add = False
                break
        
        if add:
            filtered.append(cani)

    print(len(filtered))

    """ SORT AND COMBINE """

    sorted_candidates = sorted(filtered, key=lambda c: c.song_descriptor_index)

    print(len(sorted_candidates))

    max_offset_secs = 2
    max_offset = max_offset_secs * descriptors_per_second
    max_combine_dist_secs = 3
    max_combine_distance = max_combine_dist_secs * descriptors_per_second

    for i in range(len(sorted_candidates)):
        copy_i = sorted_candidates[i]
        for j in range(i + 1, len(sorted_candidates)):
            copy_j = sorted_candidates[j]

            if (copy_i.distance(copy_j) <= max_combine_distance) and (copy_i.offset_diff(copy_j) <= max_offset):
                copy_i.combine(copy_j)

    print(len(sorted_candidates))

    """ OVERLAPPED """

    repeated = set()
    off_set_diff_limit_secs = 10
    off_set_diff_limit = off_set_diff_limit_secs * descriptors_per_second
    max_overlap_dist_secs = 3
    max_overlap_distance = max_overlap_dist_secs * descriptors_per_second

    for i in range(len(sorted_candidates)):
        copy_i = sorted_candidates[i]
        for j in range(i + 1, len(sorted_candidates)):
            copy_j = sorted_candidates[j]

            if copy_i.distance(copy_j) <= max_overlap_distance and copy_i.offset_diff(copy_j) <= off_set_diff_limit_secs:
                if copy_i.sequence_duration >= copy_j.sequence_duration:
                    repeated.add(copy_j)
                else:
                    repeated.add(copy_i)

    for copy in repeated:
        sorted_candidates.remove(copy)

    print(len(sorted_candidates))

    """ DELETE SHORT COPIES """
    
    filtered_copies = []

    for copy in sorted_candidates:
        if copy.sequence_duration > min_duration:
            filtered_copies.append(copy)

    print(len(filtered_copies))

    """ SHOW SEQUENCES """

    import datetime

    print("Song secs | Movie secs")

    for match in filtered_copies:
        print(f"{str(datetime.timedelta(seconds=match.song_sequence_start_time))} - {str(datetime.timedelta(seconds=match.song_end_index() * descriptors_per_second))} | {str(datetime.timedelta(seconds=match.movie_sequence_start_time))} - {str(datetime.timedelta(seconds=match.movie_end_index() * descriptors_per_second))}")
