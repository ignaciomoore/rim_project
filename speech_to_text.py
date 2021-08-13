"""
import speech_recognition as sr

r = sr.Recognizer()

filename = "debra_song.22000.wav"

with sr.AudioFile(filename) as source:
    # listen for the data (load audio to memory)
    audio_data = r.record(source)
    # recognize (convert from speech to text)
    text = r.recognize_google(audio_data)
    print(text)
"""

"""
with sr.Microphone() as source:
    print("Speak Anything: ")
    audio = r.listen(source)

    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")

    except:
        print("Sorry could not recognize your voice")
"""
