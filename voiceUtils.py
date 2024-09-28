import os
from dotenv import load_dotenv
import sounddevice as sd
import numpy as np
import queue
from groq import Groq

# Load environment variables from .env file
load_dotenv()

# Initialize Groq client with API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Audio capture settings
SAMPLE_RATE = 16000  # Whisper models typically use 16 kHz
DURATION = 5  # Duration of audio chunk to capture (seconds)

# Create a queue to store audio data
audio_queue = queue.Queue()

# Callback function to capture audio in real time
def audio_callback(indata, frames, time, status):
    if status:
        print(f"Error: {status}")
    audio_queue.put(indata.copy())

def real_time_transcription():
    # Start streaming audio from the microphone
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, callback=audio_callback):
        print("Listening... Press Ctrl+C to stop.")
        
        try:
            while True:
                # Capture audio from the queue
                audio_data = audio_queue.get()
                
                # Convert the audio data to a format Whisper can handle
                audio_bytes = np.frombuffer(audio_data, dtype=np.float32).tobytes()

                # Send the audio to Groq's Whisper model for transcription
                transcription = client.audio.transcriptions.create(
                    file=("realtime_audio.wav", audio_bytes),  # Use captured audio
                    model="distil-whisper-large-v3-en",  # Whisper model for transcription
                    response_format="json",
                    language="en"  # Optional: set language
                )

                # Print or return the transcription
                print(transcription['text'])

        except KeyboardInterrupt:
            print("\nTranscription stopped.")

# Run the real-time transcription function
real_time_transcription()
