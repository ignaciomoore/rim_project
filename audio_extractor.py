
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

if __name__ == "__main__":

    # python audio_extractor.py {video path} {audio name}

    if len(sys.argv) > 2:
        video_path = sys.argv[1]
        audio_name = sys.argv[2]

        sample_rate = 22000  # <- change here
        audio_paths = "audios"

        if not os.path.isdir(audio_paths):
            os.mkdir(audio_paths)

        audio = extract_audio(video_path, sample_rate, f"{audio_paths}/{audio_name}")

        print(f"Audio extracted: {audio_paths}/{audio_name}")
