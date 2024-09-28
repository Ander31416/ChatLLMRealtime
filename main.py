import os
import time
from AudioRecorder import record_audio_GUI
from LLM import LLM
from utils import get_file_path, record_audio_realtime, speech_to_text, text_to_speech, text_to_speech_by_chunks
from visionUtils import image_to_base64

llm = LLM(service="Groq", model="llava-v1.5-7b-4096-preview")
#llm = LLM(service="OpenAI", model="gpt-4o-mini")
llm = LLM(service="Together.ai", model="meta-llama/Llama-Vision-Free")

TTS_tool = "Google TTS"
#TTS_tool = "ElevenLabs"

while True:
    while not (os.path.exists(get_file_path("input.mp3")) and os.path.exists(get_file_path("photo_from_camera.png"))):
        pass

    time.sleep(0.001)

    input_text = speech_to_text(get_file_path("input.mp3"))
    input_image = image_to_base64(get_file_path("photo_from_camera.png"))

    response = llm.process_image_and_text(input_image, input_text)

    text_to_speech_by_chunks(TTS_tool, response, "en")

    os.remove(get_file_path("input.mp3"))
    os.remove(get_file_path("photo_from_camera.png"))