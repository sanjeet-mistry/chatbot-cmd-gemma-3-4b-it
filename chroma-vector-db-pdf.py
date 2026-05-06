import fitz  # PyMuPDF
from embeddings_old import calculate_embeddings
import chromadb
from sentence_transformers import CrossEncoder
from chat import Chat
from data import Data

doc = fitz.open(
    "./week-3/chatbot-cmd-class/data/harry-potter-and-the-sorcerer's-stone.pdf")

all_text = ""

for page in doc:
    text = page.get_text()
    all_text += text


def chunk_text_overlap(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))

    return chunks


chunks = chunk_text_overlap(all_text)
embeddings_array = calculate_embeddings("array", chunks)

questions = [
    # Easy
    "What is the full name of Harry’s uncle?",
    "Where do the Dursleys live?",
    "What is the name of Dudley’s school?",
    "What animal escapes from the zoo?",
    "What is the name of the street where Harry lives?",

    # Medium
    "Why does Mr. Dursley feel uneasy on his way to work at the beginning of the story?",
    "What unusual events are reported on the news the night Harry arrives at the Dursleys’ house?",
    "Why does Harry have to go to the zoo with the Dursleys?",
    "What does the snake say (or imply) to Harry at the zoo?",
    "Why does Professor McGonagall think leaving Harry with the Dursleys is a bad idea?",

    # Hard
    "How does Dumbledore explain why Harry should grow up away from fame?",
    "What clues in the first chapter suggest something unusual has happened in the wizarding world?",
    "How do the Dursleys treat Harry differently compared to Dudley? Give specific examples.",
    "What evidence shows that Harry has magical abilities before he knows he is a wizard?",

    # Very Hard
    "Explain how the author builds tension about Voldemort’s disappearance using multiple perspectives (e.g., news, conversations, and observations)."
]

questions_embeddings_array = embeddings.calculate_embeddings(
    "array", questions)

reranker = CrossEncoder("./models/bge-reranker-base")
client = chromadb.Client()
collection = client.create_collection(name="my_docs")
for i, doc in enumerate(chunks):
    collection.add(
        documents=[doc],
        embeddings=[embeddings_array[i]],
        ids=[str(i)]
    )
chat1 = Chat("query", Data.user_info, None, Data.assistant_chat_params, 0)

for question, question_embedding in zip(questions, questions_embeddings_array):
    results = collection.query(
        query_embeddings=question_embedding,
        n_results=10
    )

    docs = results["documents"][0]

    pairs = [[question, doc] for doc in docs]

    # Step 3: Rerank
    scores = reranker.predict(pairs)

    # Step 4: Sort by score
    ranked_docs = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

    # Step 5: Take top
    top_docs = [doc for doc, score in ranked_docs[:5]]
    print(f"Question: {question}")
    response = chat1.generate_output(question, top_docs)
    print(f"Answer: {response}\n")
