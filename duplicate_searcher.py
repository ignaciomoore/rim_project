
class Candidate:
    sequence_duration = 0
    missing_descriptors = 0
    found_descriptors = 0
    missing_streak = 0

    def __init__(self, song_descriptor_index, movie_descriptor_index, sample_rate):
        self.song_descriptor_index = song_descriptor_index
        self.movie_descriptor_index = movie_descriptor_index
        self.next_movie_descriptor_index = movie_descriptor_index + 1
        self.song_sequence_start_time = self.song_descriptor_index / sample_rate
        self.movie_sequence_start_time = self.movie_descriptor_index / sample_rate

    def find_next(self, neighbours_list):
        if self.next_movie_descriptor_index in neighbours_list:
            self.missing_streak = 0
            self.found_descriptors += 1
        else:
            self.missing_streak += 1
            self.missing_descriptors += 1
        self.next_movie_descriptor_index += 1
        self.sequence_duration += 1

    def offset_diff(self, other):
        return abs((other.movie_descriptor_index - other.song_descriptor_index) -
                   (self.movie_descriptor_index - self.song_descriptor_index))

    def contains(self, other):
        if (self.song_descriptor_index <= other.song_descriptor_index) and \
                (self.movie_descriptor_index <= other.movie_descriptor_index) and \
                (self.song_descriptor_index + self.sequence_duration >=
                 other.song_descriptor_index + other.sequence_duration) and \
                (self.movie_descriptor_index + self.sequence_duration >=
                 other.movie_descriptor_index + other.sequence_duration):
            return True
        else:
            return False

    def distance(self, other):
        if (self.song_descriptor_index in range(other.song_descriptor_index,
                                                other.song_descriptor_index + other.sequence_duration) or
                (self.song_descriptor_index + self.sequence_duration in range(other.song_descriptor_index,
                                                                              other.song_descriptor_index + other.sequence_duration)) or
                (other.song_descriptor_index in range(self.song_descriptor_index,
                                                      self.song_descriptor_index + self.sequence_duration)) or
                (other.song_descriptor_index + other.sequence_duration in range(self.song_descriptor_index,
                                                                                self.song_descriptor_index + self.sequence_duration))):
            return 0
        else:
            return abs(min((other.song_descriptor_index - self.song_descriptor_index + self.sequence_duration),
                           (self.song_descriptor_index - other.song_descriptor_index + other.sequence_duration)))

    def combine(self, other):
        combination = Candidate(min(self.song_descriptor_index, other.song_descriptor_index),
                                min(self.movie_descriptor_index, other.movie_descriptor_index))
        combination.sequence_duration = self.sequence_duration + other.sequence_duration - self.offset_diff(other)
        return combination
