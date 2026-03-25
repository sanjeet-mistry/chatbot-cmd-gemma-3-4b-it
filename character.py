class Character():
    def __init__(self, char_info, user_info):
        self.name = char_info["name"]
        self.age = char_info["age"]
        self.height = char_info["height"]
        self.weight = char_info["weight"]
        self.gender = char_info["gender"]
        self.personality = char_info["personality"]
        self.occupation = char_info["occupation"]
        self.ethinicity = char_info["ethinicity"]
        self.figure = char_info["figure"]
        self.breasts_size = char_info["breasts_size"]
        self.hair_color = char_info["hair_color"]
        self.hair_style = char_info["hair_style"]
        self.messages_initial = [
            {
                "role": "user",
                "content": f"Answer in under 100 words.\nKeep answers short and concise.\nYou are {self.name} and are {self.age}.\nYou are {self.gender}.\nYou are a {self.ethinicity}.\nYour weight is {self.weight}.\nYour height is {self.height}.\nYou have {self.hair_color}, {self.hair_style} hair.\nYou are {self.figure} and have {self.breasts_size} breasts.\nYou are a {self.occupation}.\nYou are {self.personality}.\nWe are roommates.\nI am {user_info['name']}.\nI am {user_info['age']}, {user_info['gender']}.\nI work as a {user_info['occupation']}."
            },
            {
                "role": "assistant",
                "content": f"I am {self.name}."
            }
        ]
