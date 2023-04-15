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


# List available voices
voices = engine.getProperty('voices')
for voice in voices:
    print(f"Voice ID: {voice.id}, Name: {voice.name}, Lang: {voice.languages}")

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
print(f"Recording for {DURATION} seconds...")
frames = []
for _ in range(0, int(SAMPLE_RATE / CHUNK * DURATION)):
    data = stream.read(CHUNK)
    frames.append(data)

# Stop the audio stream
stream.stop_stream()
stream.close()
audio.terminate()
engine.setProperty('voice', voices[2].id)
# Save the audio to a file
with wave.open("loopback_output.wav", "wb") as wav_file:
    wav_file.setnchannels(CHANNELS)
    wav_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    wav_file.setframerate(SAMPLE_RATE)
    wav_file.writeframes(b"".join(frames))

# Transcribe the audio using speech_recognition
with sr.AudioFile("loopback_output.wav") as source:
    audio_data = recognizer.record(source)
    text = recognizer.recognize_google(audio_data)
    text_to_translate = text

    print("Times Up....")
    translated_text = GoogleTranslator(source='en', target='es').translate(text_to_translate)
    engine.say(translated_text)
    engine.runAndWait()
    print("Transcription:", text, translated_text)