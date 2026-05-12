from core.embeddings_old import calculate_embeddings
import fitz
from core.utils import chunk_text_overlap
from core.embeddings_old import calculate_embeddings

file_name = "./week-3/chatbot-cmd-class/data/sherlock-holmes.txt"

with fitz.open(file_name) as doc:
    all_text = ""
    for page in doc:
        all_text += page.get_text()

chunks = chunk_text_overlap(all_text)
calculate_embeddings(
    "array", chunks, "sherlock-holmes-300-75")
