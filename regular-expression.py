import fitz
import re
from core.utils import chunk_text_overlap
from core.embeddings_old import calculate_embeddings

file_name = "./week-3/chatbot-cmd-class/data/harry-potter-and-the-sorcerer-stone.pdf"

current_chapter = None
chapter_start_pattern = r"C H A P T E R[\s]+[A-Z]+"


def extract_and_clean_page_content(page_blocks, pdf_page):
    global current_chapter
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
        # chapter page
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


pages = []
chunks = []

with fitz.open(file_name) as doc:
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

for index, page in enumerate(pages):
    chapter_title = ""
    if "chapter-title" in page:
        chapter_title = page["chapter-title"]
        text = chapter_title + "\n\n" + page["chapter-text"]
        if (index == 0):
            print(text)
    else:
        text = page["chapter-text"]
    text_chunks = chunk_text_overlap(text)
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

calculate_embeddings(
    "array", chunks_text, "harry-potter-and-the-sorcerer-stone-200-50")
