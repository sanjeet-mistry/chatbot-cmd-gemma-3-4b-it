from embeddings_old import calculate_embeddings
import fitz
from utils import chunk_text_overlap
from embeddings_old import calculate_embeddings

file_name = "./week-3/chatbot-cmd-class/data/harry-potter-and-the-sorcerer's-stone.pdf"

with fitz.open(file_name) as doc:
    all_text = ""
    for page in doc:
        all_text += page.get_text()

chunks = chunk_text_overlap(all_text, 250, 60)
calculate_embeddings(
    "array", chunks, "harry-potter-and-the-sorcerer-stone-250-60")
