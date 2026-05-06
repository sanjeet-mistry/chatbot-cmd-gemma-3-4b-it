import fitz  # PyMuPDF
from chat import Chat
from data import Data
from utils import chunk_text_overlap
from chroma_vector_db import ChromaVectorDB
import json

collection_file_name = "harry-potter-and-the-sorcerer-stone"
collection_file_path = "./week-3/chatbot-cmd-class/chroma-db/"

doc = fitz.open(
    "./week-3/chatbot-cmd-class/data/harry-potter-and-the-sorcerer's-stone.pdf")

all_text = ""

for page in doc:
    text = page.get_text()
    all_text += text

chunks = chunk_text_overlap(all_text)

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

with open("./week-3/chatbot-cmd-class/generated/harry-potter-and-the-sorcerer's-stone.json") as file:
    embeddings_array = json.load(file)["embeddings"]

chromaVectorDB = ChromaVectorDB()
# chromaVectorDB.create_collection(
#     chunks, embeddings_array, collection_file_path, collection_file_name)
# chat1 = Chat("query", Data.user_info, None, Data.assistant_chat_params, 0)

results = chromaVectorDB.return_best_results(
    collection_file_name, collection_file_path, questions, 6, True, 3)
print(results)
