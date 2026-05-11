import chromadb
from sentence_transformers import SentenceTransformer, CrossEncoder
from core.chat import Chat
from data import Data
import torch

# -------------------------
# Load data
# -------------------------
texts = []
with open("./week-3/chatbot-cmd-class/data/swapnil-info.txt", encoding="utf-8") as f:
    for line in f:
        texts.append(line.strip())

# -------------------------
# Models
# -------------------------
embedding_model = SentenceTransformer("./models/bge-large-en-v1.5")

# 🔥 RERANKER MODEL
reranker = CrossEncoder("./models/bge-reranker-base")

# -------------------------
# Create embeddings
# -------------------------
embeddings = embedding_model.encode(texts)

# -------------------------
# ChromaDB setup
# -------------------------
client = chromadb.Client()
collection = client.create_collection(name="my_docs")

for i, doc in enumerate(texts):
    collection.add(
        documents=[doc],
        embeddings=[embeddings[i]],
        ids=[str(i)]
    )

# -------------------------
# Questions
# -------------------------
questions = [
    "What is Swapnil’s profession?",
    "Where does Swapnil live in Mumbai?",
    "What is Swapnil’s favorite food?",
    "Which football club does Swapnil support?",
    "Which mobile phone does Swapnil use?",
    "What time does Swapnil usually wake up?",
    "Which app does Swapnil prefer for listening to music?",
    "What transport does Swapnil use for his daily commute, and from which station does he board?",
    "What are Swapnil’s favorite sports and the players he admires in them?",
    "If Swapnil plans a relaxed evening with his favorite activities, what might he do, where might he go, and what could he eat or drink?"
]

# -------------------------
# Query + Rerank
# -------------------------
context_array = []
for question in questions:
    query_embedding = embedding_model.encode([question])

    # Step 1: Retrieve more candidates
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=20   # 🔥 increased for reranker
    )

    docs = results["documents"][0]

    # Step 2: Prepare pairs (query, doc)
    pairs = [[question, doc] for doc in docs]

    # Step 3: Rerank
    scores = reranker.predict(pairs)

    # Step 4: Sort by score
    ranked_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

    # Step 5: Take top 7
    top_docs = [doc for doc, score in ranked_docs[:7]]
    context_array.append(top_docs)


torch.cuda.empty_cache()
chat1 = Chat("query", Data.user_info, None,
             Data.assistant_chat_params, 0, "gemma-4-e4b-it")
for question, top_docs in zip(questions, context_array):
    print(f"Question: {question}")
    for doc in top_docs:
        print("-", doc)
    response = chat1.generate_output(question, top_docs)
    print(f"Answer: {response}\n")
