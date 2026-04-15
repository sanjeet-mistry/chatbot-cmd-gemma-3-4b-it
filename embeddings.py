from sentence_transformers import SentenceTransformer
import numpy as np


def return_similarity_scores(file_type="array", file=None, query="", number=1):
    model = SentenceTransformer("./models/bge-large-en-v1.5")
    texts_output = []
    if file_type == "text":
        with open(file, encoding='utf-8') as f:
            for line in f:
                obj = {
                    "text": line.rstrip("\n"),
                    "similarity": None
                }
                texts_output.append(obj)
    elif file_type == "json":
        import json
        with open(file, 'r') as f:
            data = json.load(f)
        texts_only = []
        for obj in data:
            text = f"""
Laptop information:
Name: {obj["name"]}
Category: {obj["category"]}
CPU: {obj["specs"]["cpu"]}, CPU score: {obj["specs_score"]["cpu"]}
RAM: {obj["specs"]["ram"]}, RAM score: {obj["specs_score"]["ram"]}
GPU: {obj["specs"]["gpu"]}, GPU score: {obj["specs_score"]["gpu"]}
Storage: {obj["specs"]["storage"]}, Storage score: {obj["specs_score"]["storage"]}
Display: {obj["specs"]["display"]}, Display score: {obj["specs_score"]["display"]}
Total score: {obj["specs_score"]["cpu"] + obj["specs_score"]["ram"] + obj["specs_score"]["gpu"] + obj["specs_score"]["storage"] + obj["specs_score"]["display"]}
Price: {obj["price"]}"""
            obj = {
                "text": text,
                "similarity": None
            }
            texts_only.append(text)
            texts_output.append(obj)
    elif file_type == "chat":
        with open(file, encoding='utf-8') as f:
            text = f.read()
            messages = text.split("\n\n")
            messages = [message for message in messages if message != ""]
            print(messages)
    elif file_type == "array":
        for text in file:
            obj = {
                "text": text,
                "similarity": None
            }
            texts_output = texts_output.append(obj)
    texts_only = [item["text"] for item in texts_output]
    embeddings = model.encode(texts_only)
    query_embedding = model.encode(query)

    magA = np.linalg.norm(query_embedding)
    scores = np.array([])
    for i in np.arange(len(texts_output)):
        magB = np.linalg.norm(embeddings[i])
        dot = np.dot(query_embedding, embeddings[i])
        scores = np.append(scores,  dot / (magA * magB))

    for i in np.arange(len(texts_output)):
        texts_output[i]["similarity"] = float(scores[i])

    result = sorted(
        texts_output, key=lambda x: x["similarity"], reverse=True)

    return result[:number]
