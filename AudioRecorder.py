import pyaudio
import wave
import threading
import time
import tkinter as tk
from tkinter import messagebox

class AudioRecorder:
    def __init__(self):
        self.chunk = 1024  # Audio chunk size
        self.sample_format = pyaudio.paInt16  # 16-bit depth
        self.channels = 1  # Mono audio
        self.rate = 44100  # Sample rate (44.1 kHz)
        self.filename = "input.mp3"  # Output file name
        self.recording = False
        self.frames = []

        self.p = pyaudio.PyAudio()
        self.stream = None

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.frames = []
            self.stream = self.p.open(format=self.sample_format, channels=self.channels, rate=self.rate,
                                       frames_per_buffer=self.chunk, input=True)

            thread = threading.Thread(target=self.record)
            thread.start()

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.stream.stop_stream()
            self.stream.close()

            # Save the recorded audio to a file
            with wave.open(self.filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.p.get_sample_size(self.sample_format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.frames))

            print(f"Audio saved as {self.filename}")

    def record(self):
        while self.recording:
            try:
                data = self.stream.read(self.chunk)
                self.frames.append(data)
            except Exception as e:
                print(f"Error: {str(e)}")

def record_audio_GUI():
    # Create a simple GUI to start and stop the recording
    window = tk.Tk()
    window.title("Audio Recorder")
    window.geometry("400x200")  # Set the window size
    window.configure(background="#f2f2f2")  # Set the window background color

    recorder = AudioRecorder()

    def start_recording():
        recorder.start_recording()
        button.config(text="Stop Recording")
        button.config(command=stop_recording, bg="#ff0000")  # Change the button color when recording
        status_label.config(text="Recording...", fg="#ff0000")

    def stop_recording():
        recorder.stop_recording()
        button.config(text="Start Recording")
        button.config(command=start_recording, bg="#007bff")  # Change the button color when not recording
        status_label.config(text="Not Recording", fg="#007bff")  # Changed the color to blue

    button = tk.Button(window, text="Start Recording", command=start_recording, font=("Arial", 16), bg="#007bff", fg="#ffffff", width=15)
    button.pack(pady=20)

    status_label = tk.Label(window, text="Not Recording", font=("Arial", 14), fg="#007bff", bg="#f2f2f2")  # Changed the color to blue
    status_label.pack(pady=20)

    window.mainloop()
    recorder.p.terminate()

if __name__ == "__main__":
    record_audio_GUI()