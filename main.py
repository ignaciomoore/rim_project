import time
import sys
import numpy
from scipy.spatial import distance
from prettytable import PrettyTable
import datetime

from song_searcher import play_result
from duplicate_searcher import Candidate
from duplicate_searcher import Neighbours
from song_searcher import get_closest_neighbours


def run_process(descriptors_file, seq_len="", num_neighs="", same_audio=True):

    """ READING DESCRIPTORS """

    print("Reading descriptors ...", end="\r")

    if same_audio:
        descriptors_file_path = descriptors_file
        info_extractor = descriptors_file_path.split("_")
        number_of_descriptors = int(info_extractor[-1].split(".")[0])
        descriptors_per_second = int(info_extractor[-2])

        t0 = time.time()
        
        descriptors_shape = (number_of_descriptors, 32)

        descriptors = numpy.fromfile(descriptors_file_path, sep="\n").reshape(descriptors_shape)
        t1 = time.time()

        print(f"    Descriptors {descriptors.shape} | {round(t1-t0, 2)} secs", end="\r")
    
    else:
        descriptors_file_path_1 = descriptors_file[0]
        info_extractor_1 = descriptors_file_path_1.split("_")
        number_of_descriptors_1 = int(info_extractor_1[-1].split(".")[0])
        descriptors_per_second = int(info_extractor_1[-2])

        t0 = time.time()
        
        descriptors_shape_1 = (number_of_descriptors_1, 32)

        descriptors_1 = numpy.fromfile(descriptors_file_path_1, sep="\n").reshape(descriptors_shape_1)
        t1 = time.time()

        print(f"    Descriptors {descriptors_1.shape} | {round(t1-t0, 2)} secs", end="\r")

        descriptors_file_path_2 = descriptors_file[1]
        info_extractor_2 = descriptors_file_path_2.split("_")
        number_of_descriptors_2 = int(info_extractor_2[-1].split(".")[0])

        t0 = time.time()
        
        descriptors_shape_2 = (number_of_descriptors_2, 32)

        descriptors_2 = numpy.fromfile(descriptors_file_path_2, sep="\n").reshape(descriptors_shape_2)
        t1 = time.time()

        print(f"    Descriptors {descriptors_2.shape} | {round(t1-t0, 2)} secs", end="\r")

    """ CALCULATE DISTANCES """

    print("Calculating distances ...")

    t0 = time.time()
    if same_audio:
        distances = distance.cdist(descriptors, descriptors)
    else:
        distances = distance.cdist(descriptors_1, descriptors_2)
    t1 = time.time()

    print(f"    Distances {distances.shape} | {round(t1-t0, 2)} secs", end="\r")

    """ GET NEIGHBOURS """

    print("Obtaining closest neighbours ...", end="\r")

    if num_neighs != "":
        number_of_neighbours = int(num_neighs)
    else:
        number_of_neighbours = 10
    min_offset_seconds = 60
    min_offset_descriptors = min_offset_seconds * descriptors_per_second

    neighbours = []
    total = distances.shape[0]
    t10 = time.time()
    
    for i in range(distances.shape[0]):
        print(f"    Progress: {round((i/total)*100, 2)}%", end="\r")
        if same_audio:
            neighs = get_closest_neighbours(i, number_of_neighbours, distances, min_offset_descriptors)
        else:
            neighs = numpy.argpartition(distances[i], number_of_neighbours)[:number_of_neighbours]
        neighbours.append(neighs)
    
    t11 = time.time()
    neighbours = Neighbours(numpy.array(neighbours))
    print(f"    Neighbours {neighbours.shape()} | {round(t11-t10, 2)} secs", end="\r")

    """ CREATE CANDIDATES """

    print("Creating candidates ...", end="\r")

    candidates = []
    song_indexes = range(distances.shape[0])
    total_songs = distances.shape[0]
    for song in song_indexes:
        print(f"    Progress {round((song/total_songs)*100, 2)}%", end="\r")
        for neighbour in neighbours.search(song):
            candidates.append(Candidate(song, neighbour, descriptors_per_second))

    print(f"    Candidates {len(candidates)}", end="\r")

    """ FIND SEQUENCE """

    print("Finding sequences ...", end="\r")

    copies = []

    max_missing_streak_secs = 1
    max_missing_streak = max_missing_streak_secs * descriptors_per_second
    
    if seq_len != "":
        min_duration_seconds = int(seq_len)
    else:
        min_duration_seconds = 3
    min_duration = min_duration_seconds * descriptors_per_second

    total_candidates = len(candidates)
    t0 = time.time()
    
    for i in range(len(candidates)):
        print(f"    Progress {round((i/total_candidates)*100, 2)}%", end="\r")
        cand = candidates[i]
        current_candidate = cand.find_next(neighbours, max_missing_streak, min_duration)
        if current_candidate.sequence_duration >= min_duration and current_candidate.score() >= 1:
            copies.append(current_candidate)
    t1 = time.time()
    print(f"    Sequences {len(copies)} | {round(t1-t0, 2)} secs", end="\r")   

    """ CONTAIN """

    print("Contain ...", end="\r")

    filtered = []

    for i in range(len(copies)):
        print(f"    Progress {round((i/len(copies))*100, 2)}%", end="\r")
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

    print(f"    {len(filtered)}", end="\r")

    """ SORT AND COMBINE """

    print("Sort and combine ...", end="\r")

    sorted_candidates = sorted(filtered, key=lambda c: c.song_descriptor_index)

    print(f"    {len(sorted_candidates)}", end="\r")

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

    print(f"    {len(sorted_candidates)}", end="\r")

    """ OVERLAPPED """

    print("Overlaping ...", end="\r")

    repeated = set()
    off_set_diff_limit_secs = 10
    off_set_diff_limit = off_set_diff_limit_secs * descriptors_per_second
    max_overlap_dist_secs = 3
    max_overlap_distance = max_overlap_dist_secs * descriptors_per_second

    for i in range(len(sorted_candidates)):
        copy_i = sorted_candidates[i]
        for j in range(i + 1, len(sorted_candidates)):
            copy_j = sorted_candidates[j]

            if copy_i.distance(copy_j) <= max_overlap_distance and copy_i.offset_diff(copy_j) <= off_set_diff_limit:
                if copy_i.sequence_duration >= copy_j.sequence_duration:
                    repeated.add(copy_j)
                else:
                    repeated.add(copy_i)

    for copy in repeated:
        sorted_candidates.remove(copy)

    print(f"    {len(sorted_candidates)}", end="\r")

    """ DELETE SHORT COPIES """

    print("Deleting short copies ...", end="\r")
    
    filtered_copies = []

    for copy in sorted_candidates:
        if copy.sequence_duration > min_duration:
            filtered_copies.append(copy)

    print(f"    {len(filtered_copies)}", end="\r")

    """ GET AVERAGE DISTANCES """

    print("Calculating average distances ...", end="\r")

    for match in filtered_copies:
        match.avg_distance(distances)

    sorted_and_filtered = sorted(filtered_copies, key=lambda c: c.avg_distance)
    print("Done", end="\r")
    return sorted_and_filtered, descriptors_per_second

def show_results(descriptors_file, seq_len, num_neighs):
    myTable = PrettyTable(["Index", "Song Seconds", "Movie Seconds", "Avg Distance", "Score"])

    sorted_and_filtered, descriptors_per_second = run_process(descriptors_file, seq_len, num_neighs)

    index = 0
    for match in sorted_and_filtered:
        song_start_secs = str(datetime.timedelta(seconds=int((match.song_descriptor_index) / descriptors_per_second)))
        song_end_secs = str(datetime.timedelta(seconds=int((match.song_end_index()) / descriptors_per_second)))
        movie_start_secs = str(datetime.timedelta(seconds=int((match.movie_descriptor_index) / descriptors_per_second)))
        movie_end_secs = str(datetime.timedelta(seconds=int((match.movie_end_index()) / descriptors_per_second)))
        avg_distance = match.avg_distance    

        myTable.add_row([index, f"{song_start_secs} - {song_end_secs}", f"{movie_start_secs} - {movie_end_secs}", avg_distance, match.score()])
    
        index += 1

    print(myTable)

    watch_results = input("Watch results [y/n]: ")
    if watch_results == "y":

        video_file = input("Video file path: ")

        while True:
            play_result(video_file, sorted_and_filtered, descriptors_per_second)
            print(myTable)

    
if __name__ == "__main__":

    # python main.py {descriptor path} {seq len} {num neighs}

    """ SHOW SEQUENCES """ 

    if len(sys.argv) > 2:
        show_results(sys.argv[2], sys.argv[3], sys.argv[4])
    