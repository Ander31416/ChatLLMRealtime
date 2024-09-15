import base64

from chat import Chat
'''
import vertexai
from vertexai.generative_models import GenerativeModel, Part
import vertexai.preview.generative_models as generative_models
'''
#from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI

# Load environment variables from the .env file
#load_dotenv()

class LLM:
    def __init__(self, service, model):
        self.service = service
        self.model = model
        self.api_key = "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"#os.environ.get(f"{service.upper()}_API_KEY")  # Retrieve API key from environment variables

    def __str__(self):
        return f"{self.service} (v{self.model})"

    def generate_text(self, message):
        chat = Chat()
        chat.add_user_message(message)

        if self.service == "Groq":
            response = self.generate_text_with_groq(chat)

        if self.service == "OpenAI":
            response = self.generate_text_with_OpenAI(chat)

        if self.service == "Google":
            response = self.generate_text_with_Google(chat)

        Chat().add_assistant_message(response)
        return response

    def generate_text_with_groq(self, chat: Chat):
        client = Groq(
            api_key = self.api_key,
        )

        if not chat:
            raise ValueError("Chat cannot be empty")

        completion = client.chat.completions.create(
            model=self.model,
            messages=(chat.get_chat()),
            temperature=0.5,
            max_tokens=8000,
            top_p=1,
            stream=False,
            stop=None,
        )

        return completion.choices[0].message.content

    def generate_text_with_OpenAI(self, chat):
        client = OpenAI(
            api_key = self.api_key,
        )

        response = client.chat.completions.create(
          model=self.model,
          messages=[
            {
              "role": "system",
              "content": [
                {
                  "type": "text",
                  "text": chat["system"]
                }
              ]
            },
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": chat["user"]
                }
              ]
            }
          ],
          temperature=1,
          max_tokens=4095,
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