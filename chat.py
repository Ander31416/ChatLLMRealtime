class Chat:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Chat, cls).__new__(cls, *args, **kwargs)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.chat = []

    def add_system_message(self, message):
        self.chat.append({
            "role": "system",
            "content": message
        })

    def add_assistant_message(self, message):
        self.chat.append({
            "role": "assistant",
            "content": message
        })

    def add_user_message(self, message):
        self.chat.append({
            "role": "user",
            "content": message
        })

    def get_chat(self):
        return self.chat