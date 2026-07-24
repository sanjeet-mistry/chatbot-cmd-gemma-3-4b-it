import fitz  # PyMuPDF
import re


def extract_page_number(sample_string):
    page_match = re.search(r"\x91 (\d+) \x91", sample_string)
    if page_match:
        number = int(page_match.group(1))
    return number


def remove_new_lines(text):
    text = text.replace("-\n", "")
    # text = re.sub(r"\n([a-z])", r"\1", text)
    # text = re.sub(r"([a-z]|,)\s+([A-Z])", r"\1 \2", text)
    return text


def append_text_to_chapter(new_text):
    chapter_text = chapters[current_chapter - 1]["text"]
    match = re.search(r"([a-z]|,|Mr\.|Mrs\.|Dr\.)$", chapter_text)
    if match:
        chapters[current_chapter - 1]["text"] += " " + new_text
        return

    match2 = re.search(r"-$", chapter_text)
    if match2:
        chapters[current_chapter -
                 1]["text"] = re.sub(r"-$", "", chapter_text)
        chapters[current_chapter -
                 1]["text"] += new_text
        return

    match3 = re.search(r"[.!?]$", chapter_text)
    if match3:
        chapters[current_chapter -
                 1]["text"] += "\n" + new_text
        return

    match4 = re.search(r"”$", chapter_text)
    if match4:
        new_text_match = re.search(r"^([A-Z]|“)", new_text)
        if new_text_match:
            chapters[current_chapter - 1]["text"] += "\n" + new_text
            return
        else:
            chapters[current_chapter - 1]["text"] += " " + new_text
            return


chapters_start = False
current_chapter = 0
chapters = []

with fitz.open("./week-3/chatbot-cmd-class/data/harry-potter-and-the-sorcerer-stone.pdf") as doc:
    for index, page in enumerate(doc, start=1):
        blocks = page.get_text_blocks(sort=True)
        blocks_text = [block[4].strip() for block in blocks]
        blocks_text = [text for text in blocks_text if text]
        length = len(blocks_text)
        if length > 0:
            first = blocks_text[0]
            chapter_start_pattern = r"C H A P T E R"
            match = re.search(chapter_start_pattern, first)
            # New Chapter start page
            if match:
                if not chapters_start:
                    chapters_start = True
                current_chapter += 1

                # Extract page text
                if length == 4:
                    title = blocks_text[2]
                    title_match = re.search(r"([A-Z\-’]+\s+)+", title)
                    if title_match:
                        title = title_match.group().strip()
                        title = re.sub("\n", "", title)
                    print(title)

                    text = re.sub(r"([A-Z\-’]+\s+)+", "",
                                  blocks_text[2]).strip()

                    text = remove_new_lines(text)
                    text = blocks_text[1] + text
                    print(text)
                else:
                    title = blocks_text[1]
                    title = re.sub("\n", "", title)

                    text = ""
                    for i in range(length - 3, length - 1):
                        text += blocks_text[i]
                    text = remove_new_lines(text)

                book_page_number = extract_page_number(
                    blocks_text[length - 1])

                chapter = {
                    "pdf_page_number": index,
                    "book_page_number": book_page_number,
                    "title": title,
                    "text": text,
                    "number": current_chapter
                }
                # if index == 100:
                #     print(chapter)
                #     break
                chapters.append(chapter)
            else:
                if chapters_start:
                    length = len(blocks_text)

                    book_page_number = extract_page_number(
                        blocks_text[length - 1])

                    text = blocks_text[1]

                    append_text_to_chapter(text)

        else:
            if chapters_start:
                break


for i in range(0, len(chapters)):
    print(f"{i+1}. {chapters[i]['title']}")
