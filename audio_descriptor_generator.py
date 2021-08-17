
import os
import sys
import librosa
import time


def create_audio_descriptors(audio_file, sample_rate, dimension, window, hop):
    y, sr = librosa.load(audio_file, sample_rate)
    mfcc = librosa.feature.mfcc(y, sr=sr, n_mfcc=dimension, n_fft=window, hop_length=hop)
    return mfcc.transpose()


if __name__ == "__main__":

    # python audio_descriptor_generator.py {audio path} {descriptor file name}

    audio_file = sys.argv[1]

    sample_rate = 22000  # 44100
    descriptors_per_second = 2
    window = int(sample_rate / descriptors_per_second)  # 4096
    hop = window  # 4096
    dimension = 32

    t0 = time.time()
    descriptors = create_audio_descriptors(audio_file, sample_rate, dimension, window, hop)
    t1 = time.time()

    print(f"{round(t1 - t0, 2)} seconds")
    print(descriptors.shape)

    descriptor_paths = "descriptors"

    if not os.path.isdir(descriptor_paths):
        os.mkdir(descriptor_paths)
    
    descriptors_file = f"{sys.argv[2]}_{descriptors_per_second}_{descriptors.shape[0]}.bin"

    descriptors.tofile(f"{descriptor_paths}/{descriptors_file}", sep="\n")
    print(f"File: {descriptor_paths}/{descriptors_file}")
