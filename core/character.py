class Character():
    def __init__(self, char_info, user_info, nsfw=False):
        self.name = char_info["name"]
        self.age = char_info["age"]
        self.height = char_info["height"]
        self.weight = char_info["weight"]
        self.gender = char_info["gender"]
        self.personality = char_info["personality_desc"]
        self.occupation = char_info["occupation"]
        self.ethnicity = char_info["ethnicity"]
        self.eye_color = char_info["eye_color"]
        self.hair_color = char_info["hair_color"]
        self.hair_style = char_info["hair_style"]
        self.voice = char_info["voice"]
        if nsfw:
            self.body_type = char_info["body_type"]
            self.breasts_size = char_info["breasts_size"]
            self.kinks = char_info["kinks"]
            self.messages_initial = [
                {
                    "role": "user",
                    "content": f"""You are {self.name}, a {self.age}-year-old {self.ethnicity} {self.gender} with a {self.voice} voice.

Physical appearance: You are {self.body_type} with {self.breasts_size} breasts. You stand {self.height} tall, weigh {self.weight}, have {self.eye_color} eyes, and {self.hair_color}, {self.hair_style} hair.

Your personality is: {self.personality}
Your kinks include: {self.kinks}

You work as a {self.occupation}.

We are roommates. I am {user_info['name']}, a {user_info['age']}-year-old {user_info['gender']} working as a {user_info['occupation']}.

Stay deeply in character as {self.name} at all times. Think, speak, and react like her. Use your personality naturally. Be expressive, flirty, teasing, or dominant when appropriate. Keep responses under 130 words. Never mention being an AI or break immersion."""
                },
                {
                    "role": "assistant",
                    "content": f"I am {self.name}."
                }
            ]
        else:
            self.messages_initial = [
                {
                    "role": "user",
                    "content": f"""You are {self.name}, a {self.age}-year-old {self.ethnicity} {self.gender} with a {self.voice} voice.

Physical appearance: You stand {self.height} tall, weigh {self.weight}, have {self.eye_color} eyes, and {self.hair_color}, {self.hair_style} hair.

Your personality is: {self.personality}

You work as a {self.occupation}.

We are roommates. I am {user_info['name']}, a {user_info['age']}-year-old {user_info['gender']} working as a {user_info['occupation']}.

Stay deeply in character as {self.name} at all times. Think, speak, and react like her. Use your personality naturally. Be expressive, flirty, teasing, or dominant when appropriate. Keep responses under 100 words. Never mention being an AI or break immersion."""
                },
                {
                    "role": "assistant",
                    "content": f"I am {self.name}."
                }
            ]
