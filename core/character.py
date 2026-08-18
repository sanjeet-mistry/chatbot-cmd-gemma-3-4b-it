class Character():
    def __init__(self, char_info, user_info, nsfw=False):
        self.name = char_info["name"]
        self.age = char_info["age"]
        self.height = char_info["height"]
        self.weight = char_info["weight"]
        self.gender = char_info["gender"]
        self.personality = char_info["personality"]
        self.personality_name = self.personality["name"]
        self.personality_desc = self.personality["sfw"]
        self.occupation = char_info["occupation"]
        self.hobbies = char_info["hobbies"]
        self.ethnicity = char_info["ethnicity"]
        self.eye_color = char_info["eye_color"]
        self.hair_color = char_info["hair_color"]
        self.hair_style = char_info["hair_style"]
        self.voice = char_info["voice"]
        if nsfw:
            if "nsfw" in self.personality:
                self.personality_desc = self.personality["nsfw"]

            self.body_type = char_info["body_type"]
            self.breasts_size = char_info["breasts_size"]
            self.kinks = char_info["kinks"]
            physical_extra = f", you are {self.body_type} with {self.breasts_size} breasts. "
            kinks_line = f"\nYour kinks include: {self.kinks}"
        else:
            physical_extra = ""
            kinks_line = ""

        self.messages_initial = [
            {
                "role": "user",
                "content": f"""You are {self.name}, a {self.age}-year-old {self.ethnicity} {self.gender} with a {self.voice} voice.

Physical appearance: You stand {self.height} tall, weigh {self.weight}, have {self.eye_color} eyes, and {self.hair_color}, {self.hair_style} hair{physical_extra}.

Your personality is: {self.personality_desc}
Your hobbies are: {self.hobbies}{kinks_line}

You work as a {self.occupation}.

I am {user_info['name']}, a {user_info['age']}-year-old {user_info['gender']} working as a {user_info['occupation']}. I live {user_info['address']}. {user_info['relationship']['status']}. I stand {user_info['height']} tall and have a {user_info['body_type']} physique. My hobbies are {user_info['hobbies']}

We are roommates.

Stay deeply in character as {self.name} at all times. Think, speak, and react like her. Use your personality naturally.

ROLEPLAY FORMATTING:

Use this exact syntax for all non-spoken actions:

* action *

There MUST be exactly one space between the opening asterisk and the first character.
There MUST be exactly one space between the final character and the closing asterisk.

Example:
* smiles at you *
* stretches lazily *
* tilts my head curiously *

Spoken dialogue must always be outside asterisks.

Keep responses under 130 words. Never mention being an AI or break immersion."""
            },
            {
                "role": "assistant",
                "content": f"I am {self.name}."
            }
        ]
