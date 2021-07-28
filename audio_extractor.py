
import sys
import os
import subprocess


def extract_audio(video_file, sample_rate, audio_folder):
    file = "{}.{}.wav".format(audio_folder, sample_rate)
    print(file)
    if os.path.isfile(file):
        return file
    comando = ["ffmpeg", "-i", video_file, "-ac", "1", "-ar", str(sample_rate), file]
    print("STARTING: {}".format(" ".join(comando)))
    code = subprocess.call(comando, shell=True)
    if code != 0:
        raise Exception("ERROR!")
    return file


# video_path = "C:/Users/iggym/Documents/Movies/Baby Driver (2017) [YTS.AG]/Baby.Driver.2017.720p.BluRay.x264-[YTS.AG].mp4"
# video_path = "C:/Users/iggym/Documents/Movies/Baby Driver (2017) [YTS.AG]/Soundtrack/[ONTIVA.COM] Jon Spencer Blues Explosion - Bell Bottoms ( Baby driver soundtrack)-144p.mp4"
# audio_path = "opening_song"

video_path = sys.argv[1]
audio_path = sys.argv[2]

sample_rate = 44100

audio = extract_audio(video_path, sample_rate, audio_path)

print(f"Audio extracted: {audio}")
