import fitz  # PyMuPDF
from core.chat import Chat
from data import Data
from core.utils import chunk_text_overlap
from core.chroma_vector_db import ChromaVectorDB
import json

chunks_setting = Data.chunks[2]
collection_file_name = f"harry-potter-and-the-sorcerer-stone-{chunks_setting['size']}-{chunks_setting['overlap']}"
collection_file_path = "./week-3/chatbot-cmd-class/chroma-db/"

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

questions = [
    "What is the name of Harry’s owl?",
    "What color are Harry’s eyes?",
    "Who leaves Harry on the Dursleys’ doorstep?",
    "What present does Hagrid give Harry for his birthday?",
    "What position does Harry play in Quidditch?",

    "Why is Harry forced to live in the cupboard under the stairs?",
    "How does Harry first learn he is a wizard?",
    "Why are the Dursleys afraid of anything unusual?",
    "Describe Harry’s first meeting with Draco Malfoy.",
    "Why does Hagrid get angry in the hut on the rock?",

    "What events lead Harry to suspect Snape is trying to steal the Philosopher’s Stone?",
    "How does Harry discover that Nicolas Flamel is connected to the mystery?",
    "What clues make Hermione realize what creature is guarding the trapdoor?",
    "Why does Harry think he can trust Hagrid even when others doubt him?",
    "How does the relationship between Harry and Dudley begin to change after the zoo incident?",

    "Explain how the author gradually reveals that the wizarding world knows Harry before he knows it himself.",
    "Compare how Professor McGonagall and Hagrid feel about leaving Harry with the Dursleys.",
    "Describe the sequence of events that causes Harry to miss the train platform at King’s Cross initially.",
    "Explain how the author builds suspense around the forbidden corridor before Harry discovers what is hidden there.",
    "Trace how Harry’s opinion of Snape changes throughout the story and explain why."
]

chromaVectorDB = ChromaVectorDB()

createCollection = False

if createCollection:
    doc = fitz.open(
        "./week-3/chatbot-cmd-class/data/harry-potter-and-the-sorcerer's-stone.pdf")

    all_text = ""

    for page in doc:
        text = page.get_text()
        all_text += text

    chunks = chunk_text_overlap(all_text, chunks_setting["size"],
                                chunks_setting["overlap"])

    with open(f"./week-3/chatbot-cmd-class/generated/{collection_file_name}.json") as file:
        embeddings_array = json.load(file)["embeddings"]

    chromaVectorDB.create_collection(
        chunks, embeddings_array, collection_file_path, collection_file_name)

else:
    results = chromaVectorDB.return_best_results(
        collection_file_name, collection_file_path, questions, 20, True, {'min': 2, 'max': 6})
    chat1 = Chat("query", Data.user_info, None, Data.assistant_chat_params, 0)

    for question, result in zip(questions, results):
        print(f"Question: {question}")
        response = chat1.generate_output(question, result)
        print(f"Answer:\n{response}\n")
