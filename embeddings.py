from sentence_transformers import SentenceTransformer
import numpy as np


class Embeddings():
    def __init__(self):
        self.texts = np.array([])

    def return_similarity_scores(self, file_path=False, texts=None, query="", number=1):
        model = SentenceTransformer("./models/bge-large-en-v1.5")
        if file_path:
            with open(file_path) as file:
                for line in file:
                    obj = {
                        "text": line.rstrip("\n"),
                        "similarity": None
                    }
                    self.texts = np.append(self.texts, obj)
        else:
            for text in texts:
                obj = {
                    "text": text,
                    "similarity": None
                }
                self.texts = np.append(self.texts, obj)
        embeddings = model.encode(self.texts)
        query_embedding = model.encode(query)

        magA = np.linalg.norm(query_embedding)
        scores = np.array([])
        for i in np.arange(len(self.texts)):
            magB = np.linalg.norm(embeddings[i])
            dot = np.dot(query_embedding, embeddings[i])
            scores = np.append(scores,  dot / (magA * magB))

        for i in np.arange(len(self.texts)):
            self.texts[i]["similarity"] = float(scores[i])

        result = sorted(
            self.texts, key=lambda x: x["similarity"], reverse=True)

        return result[:number]
