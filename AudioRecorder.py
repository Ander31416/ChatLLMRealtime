import pyaudio
import wave
import threading
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2  # For accessing the camera feed
import os  # To save the files in the current directory
import numpy as np

class AudioRecorder:
    def __init__(self):
        self.chunk = 1024  # Audio chunk size
        self.sample_format = pyaudio.paInt16  # 16-bit depth
        self.channels = 1  # Mono audio
        self.rate = 44100  # Sample rate (44.1 kHz)
        self.filename = "input.mp3"  # Output audio file name
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

class ScreenRecorder:
    def __init__(self):
        self.recording = False
        self.output_file = "screen_recording.avi"  # Video file name
        self.screen_size = pyautogui.size()
        self.fps = 10  # Frames per second for screen recording
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.out = cv2.VideoWriter(self.output_file, self.fourcc, self.fps, self.screen_size)

    def start_recording(self):
        self.recording = True
        thread = threading.Thread(target=self.record_screen)
        thread.start()

    def stop_recording(self):
        self.recording = False
        self.out.release()
        print(f"Screen recording saved as {self.output_file}")

    def record_screen(self):
        while self.recording:
            img = pyautogui.screenshot()  # Capture screenshot
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)  # Convert RGB to BGR (OpenCV uses BGR)
            self.out.write(frame)

def record_audio_GUI():
    # Create a simple GUI to start and stop the recording
    window = tk.Tk()
    window.title("Audio and Screen Recorder")
    window.geometry("740x720")  # Increase the window size for the video feed and other elements
    window.configure(background="#f2f2f2")

    recorder = AudioRecorder()

    # Set up camera feed
    cap = cv2.VideoCapture(0)  # Open the default camera (change '0' if you have multiple cameras)

    # Create a frame to act as a "box" for the camera feed
    camera_frame = tk.Frame(window, width=600, height=300, bg="#000000", bd=5, relief=tk.SUNKEN)
    camera_frame.pack(pady=20)

    # Create a label inside the frame to display the camera feed
    video_label = tk.Label(camera_frame)
    video_label.pack()

    def update_camera_feed():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if ret:
            # Convert the frame to RGB (OpenCV uses BGR by default)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            video_label.imgtk = imgtk
            video_label.config(image=imgtk)

        # Continue updating the frame
        video_label.after(10, update_camera_feed)

    def take_photo(frame):
        # Save the current frame (photo) as an image file
        photo_filename = "photo_from_camera.png"
        cv2.imwrite(photo_filename, frame)
        print(f"Photo saved as {photo_filename}")

    def start_recording():
        # Capture a photo from the camera feed when recording starts
        ret, frame = cap.read()  # Capture the current frame from the camera
        if ret:
            take_photo(frame)  # Save the frame as a photo

        # Start audio recording
        recorder.start_recording()

        button.config(text="Stop Recording")
        button.config(command=stop_recording, bg="#ff0000")  # Change the button color when recording
        status_label.config(text="Recording...", fg="#ff0000")

    def stop_recording():
        # Stop audio recording
        recorder.stop_recording()

        button.config(text="Start Recording")
        button.config(command=start_recording, bg="#007bff")  # Change the button color when not recording
        status_label.config(text="Not Recording", fg="#007bff")

    # Set up buttons and labels
    button = tk.Button(window, text="Start Recording", command=start_recording, font=("Arial", 16), bg="#007bff", fg="#ffffff", width=15)
    button.pack(pady=10)

    status_label = tk.Label(window, text="Not Recording", font=("Arial", 14), fg="#007bff", bg="#f2f2f2")
    status_label.pack(pady=10)

    # Start the camera feed update loop
    update_camera_feed()

    window.mainloop()

    # Release the camera and terminate PyAudio when the window is closed
    cap.release()
    recorder.p.terminate()

if __name__ == "__main__":
    record_audio_GUI()
