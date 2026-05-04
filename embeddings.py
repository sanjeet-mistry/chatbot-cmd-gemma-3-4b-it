from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("./models/e5-base-v2")


def return_similarity_scores(texts, file_type="array", embedding=None, query="", number=1):
    embedding_array = np.array([])
    similarity = []
    for text in texts:
        obj = {
            "text": text,
            "similarity": None
        }
        similarity.append(obj)
    if file_type == "array":
        embedding_array = embedding
    elif file_type == "json":
        import json
        with open(embedding, encoding='utf-8') as file:
            data = json.load(file)
            embedding_array = np.array(data["embeddings"])

    query_embedding = model.encode(query, normalize_embeddings=True)
    magA = np.linalg.norm(query_embedding)
    scores = []
    for i in np.arange(len(embedding_array)):
        magB = np.linalg.norm(embedding_array[i])
        dot = np.dot(query_embedding, embedding_array[i])
        scores.append(dot / (magA * magB))

    scores = np.array(scores)
    for i in range(len(similarity)):
        similarity[i]["similarity"] = float(scores[i])

    result = sorted(similarity, key=lambda x: x["similarity"], reverse=True)

    return result[:number]


def calculate_embeddings(file_type, data, file_name=None):
    texts = []
    if file_type == "text":
        with open(data, encoding='utf-8') as f:
            for line in f:
                texts.append(line.rstrip("\n"))
    elif file_type == "chat":
        with open(data, encoding='utf-8') as f:
            text = f.read()
            texts = text.split("\n\n")
            texts = [message for message in texts if message != ""]
    elif file_type == "array":
        texts = data
    elif file_type == "pdf":
        import fitz
        doc = fitz.open(
            "./week-3/chatbot-cmd-class/data/Harry Potter and the Sorcerer's Stone.pdf")
        texts = ""
        for page in doc:
            text = page.get_text()
            texts += text

        print(texts[:1000])  # preview

    embeddings = model.encode(texts, normalize_embeddings=True)
    embeddings = [embedding.tolist() for embedding in embeddings]
    if file_name:
        import json
        json_data = json.dumps({"embeddings": embeddings})
        with open("./week-3/chatbot-cmd-class/generated/" + file_name + ".json", 'w') as file:
            file.write(json_data)
    else:
        return np.array(embeddings)
