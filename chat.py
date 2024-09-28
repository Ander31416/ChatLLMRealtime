class Chat:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Chat, cls).__new__(cls, *args, **kwargs)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.chat = []

    def add_system_message(self, image_base64, text):
        self.chat.append(
        {
                "role": "system",
                "content": [
                        {
                                "type": "text",
                                "text": text
                        },
                        {
                                "type": "image_url",
                                "image_url": {
                                        "url": "data:image/jpeg;base64," + image_base64
                                }
                        }
                ]
        })

    def add_assistant_message(self, text):
        self.chat.append(
        {
                "role": "assistant",
                "content": [
                        {
                                "type": "text",
                                "text": text
                        }
                ]
        })

    def add_user_message(self, image_base64, text):
        self.chat.append(
        {
                "role": "user",
                "content": [
                        {
                                "type": "text",
                                "text": text
                        },
                        {
                                "type": "image_url",
                                "image_url": {
                                        "url": "data:image/jpeg;base64," + image_base64
                                }
                        }
                ]
        })

    def get_chat(self):
        return self.chat