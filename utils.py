from gtts import gTTS
import pyaudio
import wave
from pydub import AudioSegment
from pydub.playback import play
from groq import Groq
import tempfile
import threading
import queue
from playsound import playsound
import speech_recognition as sr
import constants
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import stream
import os

# Load environment variables from .env file
load_dotenv()

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def speech_to_text(filename):
    """Transcribes audio from a file using Groq."""
    with open(filename, "rb") as file:
        transcription = client.audio.transcriptions.create(
            file=(filename, file.read()),
            model="whisper-large-v3",
            response_format="verbose_json",
        )
        return transcription.text

def process_audio(q):
    """Process audio chunks and print transcriptions."""
    while True:
        filename = q.get()
        if filename is None:
            break
        try:
            transcription = speech_to_text(filename)
            print("Transcription:", transcription)
        except Exception as e:
            print(f"Error during transcription: {e}")
        finally:
            os.remove(filename)
        q.task_done()

def record_audio_realtime():
    """Record audio in real time and transcribe it."""
    chunk = 1024  # Audio chunk size
    sample_format = pyaudio.paInt16
    channels = 1
    rate = 44100
    p = pyaudio.PyAudio()

    stream = p.open(format=sample_format, channels=channels, rate=rate, 
                    frames_per_buffer=chunk, input=True)

    audio_queue = queue.Queue()

    # Start background thread for transcription
    threading.Thread(target=process_audio, args=(audio_queue,), daemon=True).start()

    try:
        print('Recording... Press Ctrl+C to stop.')
        frames = []
        while True:
            data = stream.read(chunk)
            frames.append(data)

            if len(frames) >= int(rate / chunk * 5):  # Save every 5 seconds
                temp_wav_name = save_audio(frames, sample_format, channels, rate)
                audio_queue.put(temp_wav_name)
                frames = []  # Reset frames for the next chunk

    except KeyboardInterrupt:
        print('Recording stopped.')
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

        # Signal the transcription thread to exit
        audio_queue.put(None)
        audio_queue.join()

def save_audio(frames, sample_format, channels, rate):
    """Save audio frames to a temporary .wav file."""
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
        wf = wave.open(temp_wav.name, 'wb')
        wf.setnchannels(channels)
        wf.setsampwidth(pyaudio.PyAudio().get_sample_size(sample_format))
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()
    return temp_wav.name

def generate_speech_with_GTTS(text, lang='en'):

    # Convert text to speech
    tts = gTTS(text=text, lang=lang)

    # Save the speech to a temporary file
    file_path = get_file_path('output.mp3')
    tts.save(file_path)

    # Load the audio file
    sound = AudioSegment.from_mp3(file_path)

    #play(sound)

    # Speed up the audio
    faster_sound = sound._spawn(sound.raw_data, overrides={"frame_rate": int(sound.frame_rate * 1.25)})

    # Export the faster audio to a new file
    faster_file_path = get_file_path('output_faster.mp3')
    faster_sound.export(faster_file_path, format="mp3")

    # Play the faster audio
    play(faster_sound)

def generate_speech_with_ElevenLabs(text):

    client = ElevenLabs(
      api_key=os.environ.get("ELEVENLABS_API_KEY"), # Defaults to ELEVEN_API_KEY
    )

    audio_stream = client.generate(
      text=text,
      stream=True,
      model="eleven_multilingual_v2"
    )

    stream(audio_stream)

def text_to_speech(TTS_tool, text, language):

    text = text.replace("*", "")

    if TTS_tool == "Google TTS":
        generate_speech_with_GTTS(text, language)
    
    if TTS_tool == "ElevenLabs":
        generate_speech_with_ElevenLabs(text)

def text_to_speech_by_chunks(TTS_tool, text, language):
    try: 
        for sentence in text.split("."):
            print(sentence)
            text_to_speech(TTS_tool, sentence, language)
    except:
        print("Texto terminado")

def get_file_path(input):
    return os.path.abspath(__file__).replace("utils.py", input)


# Call the function
#record_audio()