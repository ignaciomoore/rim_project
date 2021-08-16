
import numpy

class Neighbours:
    
    def __init__(self, neighbour_matrix):
        self.neighbour_matrix = neighbour_matrix

    def shape(self):
        return self.neighbour_matrix.shape

    def search(self, song_index):
        if song_index >= self.shape()[0]:
            return 0
        return self.neighbour_matrix[song_index]
        
    
class Candidate:

    def __init__(self, song_descriptor_index, movie_descriptor_index, descriptors_per_second):
        self.song_descriptor_index = song_descriptor_index
        self.movie_descriptor_index = movie_descriptor_index

        self.song_sequence_start_time = self.song_descriptor_index / descriptors_per_second
        self.movie_sequence_start_time = self.movie_descriptor_index / descriptors_per_second

        self.next_song_descriptor_index = song_descriptor_index + 1
        self.next_movie_descriptor_index = movie_descriptor_index + 1
        self.sequence_duration = 0
        self.missing_descriptors = 0
        self.found_descriptors = 0
        self.missing_streak = 0

    def movie_end_index(self):
        return self.movie_descriptor_index + self.sequence_duration

    def song_end_index(self):
        return self.song_descriptor_index + self.sequence_duration

    def find_next(self, neighbours_list: "Neighbours", missing_streak_limit, min_sequence_duration):
        neighbours = neighbours_list.search(self.next_song_descriptor_index)
        if type(neighbours) == int:
            return self
        if self.next_movie_descriptor_index in neighbours:
            self.missing_streak = 0
            self.found_descriptors += 1
        else:
            self.missing_streak += 1
            self.missing_descriptors += 1
        
        self.next_song_descriptor_index += 1
        self.next_movie_descriptor_index += 1
        self.sequence_duration += 1

        if self.missing_streak >= missing_streak_limit:
            return self
        elif self.sequence_duration >= min_sequence_duration:
            return self
        else:
            return self.find_next(neighbours_list, missing_streak_limit, min_sequence_duration)

    def offset(self):
        return self.movie_descriptor_index - self.song_descriptor_index

    def offset_diff(self, other):
        return abs(self.offset() - other.offset())

    def contains(self, other: "Candidate"):
        movie_is_contained = self.movie_descriptor_index <= other.movie_descriptor_index and other.movie_end_index() <= self.movie_end_index()
        song_is_contained = self.song_descriptor_index <= other.song_descriptor_index and other.song_end_index() <= self.song_end_index()
        return movie_is_contained and song_is_contained

    def distance(self, other: "Candidate"):
        closest_start = numpy.clip(self.song_descriptor_index, other.song_descriptor_index, other.song_end_index())
        closest_end = numpy.clip(self.song_end_index(), other.song_descriptor_index, other.song_end_index())
        return min(abs(self.song_descriptor_index - closest_start), abs(self.song_end_index() - closest_end))

    def combine(self, other: "Candidate"):
        if self.contains(other) or other.contains(self):
            return
        
        offset_self = self.offset()
        offset_other = other.offset()

        self_end = self.song_end_index()
        other_end = other.song_end_index()
        self.sequence_duration = max(self_end, other_end) - min(self.song_descriptor_index, other.song_descriptor_index)
        self.song_descriptor_index = min(self.song_descriptor_index, other.song_descriptor_index)
        other.sequence_duration = self.sequence_duration
        other.song_descriptor_index = self.song_descriptor_index

        self.movie_descriptor_index = self.song_descriptor_index + offset_self
        other.movie_descriptor_index = other.song_descriptor_index + offset_other

        return
        
    def score(self):
        if self.found_descriptors < 3:
            return 0
        return self.found_descriptors / max(1, self.missing_descriptors - self.missing_streak)

    def avg_distance(self, distances):
        distance = []
        song_indexes = range(self.song_descriptor_index, self.song_end_index()+1)
        movie_indexes = range(self.movie_descriptor_index, self.movie_end_index()+1)
        if len(song_indexes) != len(movie_indexes):
            print("    Not the same length")
        for i in range(len(song_indexes)):
            distance.append(distances[song_indexes[i]][movie_indexes[i]])
        self.avg_distance = round(sum(distance)/len(distance), 2)

    def __str__(self):
        return f'{self.song_descriptor_index} {self.movie_descriptor_index} {self.sequence_duration} {self.score():.1f}'

    def __repr__(self):
        return str(self)