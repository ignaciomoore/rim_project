
from os import sep
import sys
import librosa
import time

def create_audio_descriptors(audio_file, sample_rate, dimension, window, hop):
    y, sr = librosa.load(audio_file, sample_rate)
    mfcc = librosa.feature.mfcc(y, sr=sr, n_mfcc=dimension, n_fft=window, hop_length=hop)
    return mfcc.transpose()

"""
def get_descriptors(video_file, sample_rate, dimension, window, hop, audio_folder):
    audio_file = extract_audio(video_file, sample_rate, audio_folder)
    descriptors = create_audio_descriptors(audio_file, sample_rate, dimension, window, hop)
    return descriptors
"""

# audio_file = "baby_driver_audio.44100.wav"
# audio_file = "C:/Users/iggym/Documents/Movies/Baby Driver (2017) [YTS.AG]/Soundtrack/Jon Spencer Blues Explosion - Bell Bottoms ( Baby driver soundtrack).mp3"
# audio_file = "opening_song.44100.wav"
audio_file = sys.argv[1]

sample_rate = 44100
window = 4096
hop = 4096
dimension = 32
t0 = time.time()
descriptors = create_audio_descriptors(audio_file, sample_rate, dimension, window, hop)
t1 = time.time()

print(t1 - t0)
print(descriptors.shape)

# descriptors_file = "opening_song_descriptors.bin"
# descriptors_file = "opening_song_descriptors.bin"
descriptors_file = sys.argv[2]
descriptors.tofile(descriptors_file, sep="\n")
