import os
import time
from AudioRecorder import record_audio_GUI
from LLM import LLM
from utils import record_audio_realtime, speech_to_text, text_to_speech, text_to_speech_by_chunks

llm = LLM(service="Groq", model="llama-3.1-8b-instant")
TTS_tool = "Google TTS"
#TTS_tool = "ElevenLabs"


while True:
    while not os.path.exists("/home/usuario/Escritorio/Visual_Studio_Code/chatVoiceRealTime/input.mp3"):
        pass

    time.sleep(0.08)

    Input = speech_to_text("/home/usuario/Escritorio/Visual_Studio_Code/chatVoiceRealTime/input.mp3")

    response = llm.generate_text(Input)

    text_to_speech_by_chunks(TTS_tool, response, "en")

    os.remove("/home/usuario/Escritorio/Visual_Studio_Code/chatVoiceRealTime/input.mp3")