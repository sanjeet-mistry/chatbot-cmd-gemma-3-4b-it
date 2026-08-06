import fitz
import re

file_name = "./week-3/chatbot-cmd-class/data/harry-potter-and-the-sorcerer-stone.pdf"

chapters = []
chapter = {}
current_chapter = 0

chapters_start = False
new_chapter_start = False
new_line_start_x = 47

with fitz.open(file_name) as doc:
    for page_num, page in enumerate(doc, start=1):
        page_lines = []
        page_dict = page.get_text("dict")
        blocks = page_dict["blocks"]
        blocks = [item for item in blocks if item["type"] == 0]
        # print(blocks)
        for block in blocks:
            lines = block["lines"]
            for line in lines:
                spans = line["spans"]
                cleaned_line = []
                for span in spans:
                    text = span["text"].strip()
                    if text != "" and text != "\x91":
                        cleaned_line.append(span)
                page_lines.append(cleaned_line)
        # if page_num == 54:
        #     print(page_lines)
        for line_index, line in enumerate(page_lines, start=1):
            for span_index, span in enumerate(line, start=1):
                if line_index == 1 and span_index == 1:
                    text = span['text']
                    if text.find("C H A P T E R") == 0:
                        if not chapters_start:
                            chapters_start = True
                        new_chapter_start = True
                        current_chapter += 1
                    else:
                        if not chapters_start:
                            break
                        new_chapter_start = False
                    if new_chapter_start:
                        chapter = {
                            "title": "",
                            "pdf_page_number": page_num,
                            "book_page_number": "",
                            "text": ""
                        }
                        chapters.append(chapter)
                else:
                    size = round(span['size'])
                    font = span['font']
                    text = span['text']
                    if size == 36 and font == "Able":
                        title = text.strip()
                        if not chapters[current_chapter - 1]['title']:
                            chapters[current_chapter - 1]['title'] = title
                        else:
                            chapters[current_chapter -
                                     1]['title'] += " " + title
                    elif size == 20 and font == "Able":
                        if new_chapter_start:
                            chapters[current_chapter -
                                     1]["book_page_number"] = int(text.strip())
                    elif (size == 13 or size == 11) and (font == "AGaramondPro-Regular" or font == "AGaramondPro-Italic" or font == "FeltTipRoman,Italic"):
                        x_pos = round(span['origin'][0])
                        chapter_text = chapters[current_chapter - 1]['text']
                        if not chapter_text:
                            chapters[current_chapter - 1]['text'] = text
                        else:
                            if span_index == 1:
                                if x_pos > new_line_start_x:
                                    chapters[current_chapter -
                                             1]['text'] += "\n" + text
                                else:
                                    chapters[current_chapter -
                                             1]['text'] = re.sub(r"([a-zA-Z]+)-$", r'\1', chapters[current_chapter -
                                                                                                   1]['text'])
                                    chapters[current_chapter -
                                             1]['text'] += text
                            else:
                                chapters[current_chapter -
                                         1]['text'] = re.sub(r"([a-zA-Z]+)-$", r'\1', chapters[current_chapter -
                                                                                               1]['text'])

                                chapters[current_chapter - 1]['text'] += text
                    elif size == 85 and font == "Able":
                        text = text.strip()
                        if (len(text) == 1):
                            chapters[current_chapter - 1]['text'] = text + \
                                chapters[current_chapter - 1]['text']

    for chapter_num, chapter in enumerate(chapters, start=1):
        chapter["text"] = f"Chapter {chapter_num}\n{chapter['title']}\n\n{chapter['text']}"
    # print(len(chapters))
    print(chapters[0]["text"])
