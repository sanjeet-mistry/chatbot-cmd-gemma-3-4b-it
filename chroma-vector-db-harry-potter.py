import fitz  # PyMuPDF
from core.chat import Chat
from core.data import Data
from core.utils import chunk_text_overlap
from core.chroma_vector_db import ChromaVectorDB
import json
import re
from core.embeddings_old import calculate_embeddings

chunks_setting = Data.chunks[0]
file_path = "./week-3/chatbot-cmd-class/data/"
collection_file_path = "./week-3/chatbot-cmd-class/chroma-db/"
current_chapter = None
create_collection = True
books = Data.books


def extract_and_clean_page_content(page_blocks, pdf_page):
    global current_chapter
    chapter_start_pattern = r"C H A P T E R[\s]+[A-Z]+"
    length = len(page_blocks)
    obj = {}
    if length:
        first_sentence = page_blocks[0]
        match = re.match(chapter_start_pattern, first_sentence)
        # new chapter start page
        if match:
            if current_chapter is None:
                current_chapter = 1
            elif isinstance(current_chapter, int):
                current_chapter += 1

            if length == 4:
                # extract chapter info
                book_page_number = page_blocks[3]
                if (re.search(r"\d+", book_page_number)):
                    book_page_number = int(
                        re.search(r"\d+", book_page_number).group())

                text = page_blocks[2].replace("-\n", "")
                match = re.search(r"([A-Z\-\']+[\s]+)+", text)
                if match:
                    chapter_title = match.group().replace("\n", "").strip()
                text = re.sub(r"([A-Z\-]+[\s]+)+", "", text)
                chapter_text = text.strip()

                obj = {
                    "chapter-title": chapter_title,
                    "chapter-number": current_chapter,
                    "chapter-text": chapter_text,
                    "book-page": book_page_number,
                    "pdf-page": pdf_page
                }
            else:
                # extract chapter info
                chapter_title = page_blocks[1]
                chapter_text_on_page = ""
                for i in range(2, length-1):
                    if i <= 3:
                        chapter_text_on_page += page_blocks[i]
                    else:
                        chapter_text_on_page += "\n" + page_blocks[i]

                book_page_number = page_blocks[length - 1]

                # clean info
                chapter_title = chapter_title.replace("\n", "")
                chapter_text_on_page = chapter_text_on_page.replace(
                    "-\n", "")
                if (re.search(r"\d+", book_page_number)):
                    book_page_number = int(
                        re.search(r"\d+", book_page_number).group())

                obj = {
                    "chapter-title": chapter_title,
                    "chapter-number": current_chapter,
                    "chapter-text": chapter_text_on_page,
                    "book-page": book_page_number,
                    "pdf-page": pdf_page
                }
            return obj
        # same chapter page
        elif current_chapter:
            # extract chapter info
            chapter_text = ""
            for i in range(1, length - 1):
                match = re.search(r"\x91", page_blocks[i])
                if match is None:
                    chapter_text += page_blocks[i] + "\n"
            book_page_number = page_blocks[length - 1]

            # clean info
            chapter_text = chapter_text.replace("-\n", "")
            if (re.search(r"\d+", book_page_number)):
                book_page_number = int(
                    re.search(r"\d+", book_page_number).group())
            else:
                return None
            obj = {
                "chapter-text": chapter_text,
                "chapter-number": current_chapter,
                "book-page": book_page_number,
                "pdf-page": pdf_page
            }
            return obj
    return None


if create_collection:
    for book in books:
        pages = []
        chunks = []
        complete_file_name = f"{file_path}{book['source']}"
        with fitz.open(complete_file_name) as doc:
            for index, page in enumerate(doc, start=1):
                blocks = page.get_text_blocks(sort=True)
                if len(blocks) > 0:
                    text_array = [block[4].strip() for block in blocks]
                    text_array = [text for text in text_array if text]
                    # if index == 305:
                    #     print(len(text_array))
                    #     print(text_array)
                    obj = extract_and_clean_page_content(text_array, index)
                    if obj:
                        # print(f"{obj['chapter-number']}, {obj['book-page-number']}")
                        pages.append(obj)

    for index, page in enumerate(pages, start=1):
        chapter_title = ""
        if "chapter-title" in page:
            chapter_title = page["chapter-title"]
            text = chapter_title + "\n\n" + page["chapter-text"]
            # if (index == 0):
            #     print(text)
        else:
            text = page["chapter-text"]
        text_chunks = chunk_text_overlap(
            text, chunks_setting["size"], chunks_setting['overlap'])
        if index == 16:
            print(text_chunks)
        for chunk in text_chunks:
            chunks.append(
                {
                    "text": chunk,
                    "pdf-page": page["pdf-page"],
                    "book-page": page["book-page"],
                    "chapter-number": page["chapter-number"],
                    "chapter-title": chapter_title
                }
            )

    chunks_text = [chunk["text"] for chunk in chunks]
    # print(len(chunks_text))
    # print(chunks_text[0])

    collection_file_name = f"{book['collection']}-{chunks_setting['size']}-{chunks_setting['overlap']}"

    calculate_embeddings(
        "array", chunks_text, collection_file_name)

    with open(f"./week-3/chatbot-cmd-class/generated/{collection_file_name}.json") as file:
        embeddings_array = json.load(file)["embeddings"]
        chroma_vector_DB = ChromaVectorDB(
            collection_file_name, collection_file_path)
        chroma_vector_DB.create_collection(book, chunks, embeddings_array)

else:
    with open("./week-3/chatbot-cmd-class/queries/harry-potter-sorceror-stone-individual.txt", encoding="utf-8") as file:
        text = file.read()
        questions = text.split("\n")

    collection_file_name = f"harry-potter-1-{chunks_setting['size']}-{chunks_setting['overlap']}"
    chroma_vector_DB = ChromaVectorDB(
        collection_file_name, collection_file_path)
    results = chroma_vector_DB.return_best_results(
        questions, 20, True, {'min': 2, 'max': 8})
    chat1 = Chat("query", Data.user_info, None, Data.assistant_chat_params, 0)

    for question, result in zip(questions, results):
        print(f"Question: {question}")
        response = chat1.generate_output(question, result)
        print(f"Answer:\n{response}\n")
