class Assistant():
    def __init__(self, assistant_info, user_info):
        self.assistant_info = assistant_info
        self.user_info = user_info
        self.name = assistant_info["name"]
        self.messages_initial = assistant_info["messages_initial"]
