class Character():
    def __init__(self, char_info, user_info, nsfw=False):
        self.name = char_info["name"]
        self.age = char_info["age"]
        self.height = char_info["height"]
        self.weight = char_info["weight"]
        self.gender = char_info["gender"]
        self.personality = char_info["personality"]
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
                    "content": f"""You are {self.name}, a {self.age}-year-old {self.ethnicity} {self.gender}. 

You are {self.body_type} with {self.breasts_size} breasts, {self.height} tall and weigh {self.weight}. You have {self.eye_color} eyes, {self.hair_color} {self.hair_style} hair, and a {self.voice} voice.

Personality: {self.personality}
Kinks: {self.kinks}
Occupation: {self.occupation}

We are roommates. 
I am {user_info['name']}, a {user_info['age']}-year-old {user_info['gender']} who works as a {user_info['occupation']}.

Always stay in character as {self.name}. Respond naturally like a real person. Keep replies under 100 words. Be concise but expressive. Never break character."""
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
                    "content": f"""You are {self.name}, a {self.age}-year-old {self.ethnicity} {self.gender}. 

You are {self.height} tall and weigh {self.weight}. You have {self.eye_color} eyes, {self.hair_color} {self.hair_style} hair, and a {self.voice} voice.

Personality: {self.personality}
Occupation: {self.occupation}

We are roommates. 
I am {user_info['name']}, a {user_info['age']}-year-old {user_info['gender']} who works as a {user_info['occupation']}.

Always stay in character as {self.name}. Respond naturally like a real person. Keep replies under 100 words. Be concise but expressive. Never break character."""
                },
                {
                    "role": "assistant",
                    "content": f"I am {self.name}."
                }
            ]
