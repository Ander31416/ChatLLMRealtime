import os
import base64

import requests

from chat import Chat
'''
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
'''
#from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI
from together import Together

# Load environment variables from the .env file
#load_dotenv()

class LLM:
    def __init__(self, service, model):
        self.service = service
        self.model = model
        self.api_key = os.environ.get(f"{service.upper()}_API_KEY")  # Retrieve API key from environment variables

    def __str__(self):
        return f"{self.service} (v{self.model})"

    def process_image_and_text(self, image_base64, text):
        chat = Chat()
        chat.add_user_message(image_base64, text)

        if self.service == "Groq":
            response = self.generate_response_groq(chat)
        elif self.service == "OpenAI":
            response = self.generate_response_openai(chat)
        elif self.service == "Together.ai":
            response = self.generate_response_togetherai(chat)
            
        Chat().add_assistant_message(response)
        return response
    
    def generate_response_togetherai(self, chat : Chat):
        client = Together(api_key=self.api_key)

        response = client.chat.completions.create(
            model=self.model,
            messages=chat.get_chat(),
            max_tokens=512,
            temperature=0.7,
            top_p=0.7,
            top_k=50,
            repetition_penalty=1,
            stop=["<|eot_id|>","<|eom_id|>"],
            stream=False
        )

        return response.choices[0].message.content

    def generate_response_groq(self, chat):
        # Create the completion request
        client = Groq(api_key=self.api_key)
        completion = client.chat.completions.create(
            model=self.model,
            messages=chat.get_chat(),
            temperature=1,
            max_tokens=4096,
            top_p=1,
            stream=False,
            stop=None
        )

        # Get the response
        response = completion.choices[0].message.content
        return response

    def generate_response_openai(self, chat):
        client = OpenAI(api_key=self.api_key)

        response = client.chat.completions.create(
            model=self.model,
            messages=chat.get_chat(),
            temperature=1,
            max_tokens=2708,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            response_format={
                "type": "text"
            }
        )

        return response.choices[0].message.content

'''
    def generate_text_with_Google(self, chat):
        vertexai.init(project="drive-automator-428421", location="us-central1")
        model = GenerativeModel(
          self.model,
        )

        generation_config = {
            "max_output_tokens": 8192,
            "temperature": 1,
            "top_p": 0.95,
        }

        safety_settings = {
            generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
            generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        }

        prompt = chat["user"]

        return model.start_chat().send_message(
            [prompt],
            generation_config=generation_config,
            safety_settings=safety_settings).candidates[0].content.parts[0].text
'''