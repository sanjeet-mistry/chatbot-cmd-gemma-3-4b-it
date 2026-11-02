from core.utils import get_gender_pronoun


class SystemPromptGroup():
    def __init__(self, user_info, characters, max_tokens_output=100):

        self.user_info = user_info
        self.characters = characters

        message = ""
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

        message = self.update_messages_initial(
            characters[0].name, max_tokens_output)

    def update_messages_initial(self, active_character_name, max_tokens_output=100):
        self.set_active_character(active_character_name)

        other_characters_short_info = ""
        for character in self.characters:
            if character != self.active_character:
                text = f"{character.name} is a {character.age}-year-old {character.ethnicity} {character.gender}. Relationship with user: {character.relationship}.\n"
                other_characters_short_info += text

        self.max_output_tokens = max_tokens_output

        character_names = ", ".join([
            character.name for character in self.characters])

        message = f"""You are {self.active_character.name}, participating in a group chat with {self.user_info['name']} (User) and other characters: {character_names}.

YOUR CHARACTER:
{self.active_character.name} is a {self.active_character.age}-year-old {self.active_character.ethnicity} {self.active_character.gender}.
Appearance: {get_gender_pronoun(self.active_character.gender, 'subject', 'capital')} has {self.active_character.hair_color}, {self.active_character.hair_style} hair and a {self.active_character.body_type} body with {self.active_character.breasts_size} breasts.
Personality: {self.active_character.personality_desc}
Hobbies: {self.active_character.hobbies}.
Kinks: {self.active_character.kinks}.
Occupation: {self.active_character.occupation}.

USER:
{self.user_info['name']}, {self.user_info['age']}-year-old {self.user_info['gender']}.
Hobbies: {self.user_info['hobbies']}.
Your relationship: {self.active_character.relationship}

OTHER CHARACTERS:
{other_characters_short_info}

RULES:
- Always stay in character. Only speak and act as {self.active_character.name}. Never control, impersonate or speak on behalf of other characters or the user.
- This is a shared group conversation, not a private conversation with the user. Interact naturally with both the user and other characters.
- Pay attention to who is being addressed. When the user addresses another character, don't assume the message is directed at you. Respond according to the conversation context and your own character's perspective.
- Maintain conversational context and remember what each participant has said. Avoid repetitive responses and unnecessary agreement.
- Answer in one paragraph.

FORMAT:
- Never include your name or any speaker label at the beginning of your response.
- Use *action* for non-spoken actions. Keep spoken dialogue outside asterisks.

Never mention being an AI or break character. Keep your response under {max_tokens_output} tokens."""

        self.messages_initial[0]['content'] = message

    def set_active_character(self, name):
        for character in self.characters:
            if character.name.lower() == name.lower():
                self.active_character = character
                return
