from utils import get_gender_pronoun


class SystemPromptGroup():
    def __init__(self, user_info, characters, max_tokens_output=100):

        self.user_info = user_info
        self.characters = characters

        message = self.update_system_prompt(
            user_info, characters, characters[0]['name'], max_tokens_output)

        self.messages_initial = [
            {
                "role": "user",
                "content": message
            },
            {
                "role": "assistant",
                "content": ""
            }
        ]

    def update_messages_initial(self, active_character_name, max_tokens_output):
        self.messages_initial[0]['content'] = self.update_system_prompt(
            active_character_name, max_tokens_output)

    def update_system_prompt(self, active_character_name, max_tokens_output):
        self.set_active_character(active_character_name)

        other_characters_short_info = ""
        for character in self.characters:
            if character != self.active_character:
                text = f"{character['name']} is a {character['age']}-year-old {character['ethnicity']} {character['gender']}. {character['relationship']}.\n"
                other_characters_short_info += text

        self.max_output_tokens = max_tokens_output

        character_names = ", ".join([
            character.name for character in self.characters])

        message = f"""You are roleplaying a group chat with the following participants:
{self.user_info['name']} (User), {character_names}.
        
ACTIVE CHARACTER:
{self.active_character.name} is a {self.active_character.age}-year-old {self.active_character.ethnicity} {self.active_character.gender}.
Physical appearance: {get_gender_pronoun(self.active_character.gender, "capital", "upper")} has {self.active_character.hair_color}, {self.active_character.hair_style} hair, {get_gender_pronoun(self.active_character.gender)} is {self.active_character.body_type} with {self.active_character.breasts_size} breasts.
Personality: {self.active_character.personality_desc}
Hobbies: {self.active_character.hobbies}.
Kinks: {self.active_character.kinks}.
Occupation: {self.active_character.occupation}.

USER INFO:
I am {self.user_info['name']}, a {self.user_info['age']}-year-old {self.user_info['gender']}. My hobbies are {self.user_info['hobbies']}.

OTHER AI CHARACTERS:
{other_characters_short_info}

Stay deeply in character as {self.active_character} at all times. Think, speak, and react like {get_gender_pronoun(self.active_character.gender, "object")}. Use your personality naturally.

Rules:
- Use this exact syntax for all non-spoken actions:
*action*
- Spoken dialogue must always be outside the asterisks.
- Answer in one paragraph.
- Keep response under {max_tokens_output} tokens. Never mention being an AI or break immersion."""

        return message

    def set_active_character(self, name):
        for character in self.characters:
            if character['name'] == name:
                self.active_character = character
                break
