import os

import keyboard as keyboard
import pyaudio
import speech_recognition as sr
import wave
from deep_translator import GoogleTranslator
import pyttsx3

# Configure the recording settings
SAMPLE_RATE = 44100
CHANNELS = 2
CHUNK = 1024
DURATION = 10  # Duration of the recording in seconds
engine = pyttsx3.init()




def case_one():
    return  "en"

def case_two():
    return "es"

def case_three():
    return "fr"

def case_four():
    return "de"

def case_five():
    return "hi"

def case_six():
    return "ta-IN"

def case_seventh():
    return "ur-IN"

def case_eigth():
    return "te-IN"

def case_ninth():
    return "bn-BD"


switch_dict = {
    1: case_one,
    2: case_two,
    3: case_three,
    4: case_four,
    5: case_five,
    6: case_six,
    7: case_seventh,
    8: case_eigth,
    9: case_ninth()
}
user_input = int(input("Please select the language you will need translating to english. \n 1 for English \n 2 for Spanish \n 3 for French \n 4 for German \n 5 for Hindi \n 6 for Tamil \n 7 for Urdu \n 8 for Telugu \n 9 for Bengali \n  "))

result = switch_dict.get(user_input)()
# Find the loopback device
audio = pyaudio.PyAudio()
loopback_device = None
for i in range(audio.get_device_count()):
    device_info = audio.get_device_info_by_index(i)
    if "Loopback" in device_info["name"] or "Stereo Mix" in device_info["name"]:
        loopback_device = device_info
        break

if not loopback_device:
    print("Loopback device not found.")
    exit()

# Initialize the recognizer
recognizer = sr.Recognizer()

# Define the audio stream
stream = audio.open(
    format=pyaudio.paInt16,
    channels=CHANNELS,
    rate=SAMPLE_RATE,
    frames_per_buffer=CHUNK,
    input=True,
    input_device_index=loopback_device["index"],
)

# Record the audio
print("Press 's' to start recording to audio you would like to translate. Press q once you are complete and want the translation...")

frames = []
recording = False

while True:
    if keyboard.is_pressed('s') and not recording:
        recording = True


    if recording:
        data = stream.read(CHUNK)
        frames.append(data)
    if keyboard.is_pressed('q'):
        break
# Stop the audio stream
stream.stop_stream()
stream.close()
audio.terminate()
#engine.setProperty('voice', voices[2].id)
# Save the audio to a file
with wave.open("loopback_output.wav", "wb") as wav_file:
    wav_file.setnchannels(CHANNELS)
    wav_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wav_file.setframerate(SAMPLE_RATE)
    wav_file.writeframes(b"".join(frames))

# Transcribe the audio using speech_recognition
with sr.AudioFile("loopback_output.wav") as source:
    audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data, language=result)
        text_to_translate = text

        print("Translating to english....")
        translated_text = GoogleTranslator(source=result, target='en').translate(text_to_translate)
        engine.say(translated_text)
        engine.runAndWait()
        print("Transcription:", text, translated_text)
    except sr.UnknownValueError:
        print("The speech recognizer could not understand the audio.")
    except sr.RequestError as e:
        print(f"Could not request results from the Google Speech Recognition service; {e}")

if os.path.exists('loopback_output.wav'):
    os.remove('loopback_output.wav')