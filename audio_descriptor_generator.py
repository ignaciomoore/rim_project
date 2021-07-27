
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

audio_file = "baby_driver_audio.8192.wav"
t0 = time.time()
descriptors = create_audio_descriptors(audio_file, 8192, 32, 4096, 4096)
t1 = time.time()

print(t1 - t0)
print(descriptors.shape)
