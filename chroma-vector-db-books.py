import fitz  # PyMuPDF
from core.chat import Chat
from core.data import Data
from core.utils import chunk_text_overlap
from core.chroma_vector_db import ChromaVectorDB
import json

chunks_setting = Data.chunks[0]
file_name = "harry-potter-and-the-sorcerer-stone"
file_path = f"./week-3/chatbot-cmd-class/data/{file_name}"
file_type = "pdf"
collection_file_name = f"{file_name}-{chunks_setting['size']}-{chunks_setting['overlap']}"
collection_file_path = "./week-3/chatbot-cmd-class/chroma-db/"

with open(f"./week-3/chatbot-cmd-class/queries/{file_name}.txt", encoding="utf-8") as file:
    text = file.read()
    questions = text.split("\n\n")

chromaVectorDB = ChromaVectorDB()
createCollection = False

if createCollection:
    if file_type == "pdf":
        doc = fitz.open(f"{file_path}.pdf")
        all_text = ""
        for page in doc:
            text = page.get_text()
            all_text += text
    elif file_type == "text":
        with open(f"{file_path}.txt", encoding="utf-8") as f:
            all_text = f.read()

    chunks = chunk_text_overlap(all_text, chunks_setting["size"],
                                chunks_setting["overlap"])

    with open(f"./week-3/chatbot-cmd-class/generated/{collection_file_name}.json") as file:
        embeddings_array = json.load(file)["embeddings"]

    chromaVectorDB.create_collection(
        chunks, embeddings_array, collection_file_path, collection_file_name)

else:
    results = chromaVectorDB.return_best_results(
        collection_file_name, collection_file_path, questions, 4, True, {'min': 2, 'max': 8})
    chat1 = Chat("query", Data.user_info, None, Data.assistant_chat_params, 0)

    for question, result in zip(questions, results):
        print(f"Question: {question}")
        response = chat1.generate_output(question, result)
        print(f"Answer:\n{response}\n")
