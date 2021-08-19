
import os
import datetime
from prettytable import PrettyTable
import numpy
from duplicate_searcher import Candidate

def get_video_names(datasets, work_path):
    new_videos = []
    for dataset in datasets:
        path = f"{work_path}dataset_{dataset}/television/"
        videos = os.listdir(path)
        new_videos_2 = []
        for video in videos:
            new_videos_2.append(video.split(".")[:-1][0])
        new_videos.append(new_videos_2)
    return new_videos


def get_video_and_audio_paths(work_path, datasets, video_names):
    video_paths = []
    audio_paths = []
    for i in range(len(datasets)):
        dataset = datasets[i]
        for video_name in video_names[i]:
            video_paths.append(f"{work_path}/dataset_{dataset}/television/{video_name}.mp4")
        audio_paths.append(f"{work_path}dataset_{dataset}/audio")

    return video_paths, audio_paths


def show(sorted_and_filtered, descriptors_per_second):
    myTable = PrettyTable(["Index", "Song Seconds", "Movie Seconds", "Avg Distance", "Score"])
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


def read_target_matrix(target_file):
    gt_values = []
    with open(target_file) as gt_file:
        for line in gt_file:
            line_split = line.split("\t")
            gt_values.append(line_split)

    return numpy.array(gt_values)


def contains(match: Candidate, start_time, end_time, descriptors_per_second, song_or_movie):
    
    if song_or_movie == "song":
        match_song_start_time = match.song_sequence_start_time
        match_song_end_time = match.song_end_index() / descriptors_per_second
        contained = start_time <= match_song_start_time and match_song_end_time <= end_time

    else:
        match_movie_start_time = match.movie_sequence_start_time
        match_movie_end_time = match.movie_end_index() / descriptors_per_second
        contained = start_time <= match_movie_start_time and match_movie_end_time <= end_time

    return contained


def get_evaluations(target_matrix, results, video_names):
    evaluation = []
    for i in range(len(results)):
        match = results[i]
        for target in target_matrix:
            if target[0] == f"{video_names[0]}.mp4":
                container = contains(match, float(target[1]), float(target[1]) + float(target[2]), 2, "song")
            else:
                container = contains(match, float(target[1]), float(target[1]) + float(target[2]), 2, "movie")
            if container:
                evaluation.append([i, target[3], 1])
            else:
                evaluation.append([i, target[3], 0])
            
    return evaluation
