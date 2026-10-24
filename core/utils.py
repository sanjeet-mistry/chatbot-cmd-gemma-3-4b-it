def chunk_text_overlap(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))

    return chunks


def chunk_text(text, chunk_size=200):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))

    return chunks


def get_gender_pronoun(gender, form="subject", case="lower"):
    pronouns = {
        "male": {"subject": "he", "object": "him"},
        "female": {"subject": "she", "object": "her"}
    }

    pronoun = pronouns[gender.lower()][form.lower()]

    if case == "capital":
        return pronoun.capitalize()
    elif case == "upper":
        return pronoun.upper()

    return pronoun
