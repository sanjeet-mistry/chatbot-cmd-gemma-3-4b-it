import fitz

file_name = "./week-3/chatbot-cmd-class/data/harry-potter-and-the-sorcerer-stone.pdf"

chapters = []
chapter = {}
current_chapter = 0

chapters_start = False
new_chapter_start = False
new_line_start_x = 47

with fitz.open(file_name) as doc:
    for page_num, page in enumerate(doc, start=1):
        page_spans = []
        page_dict = page.get_text("dict")
        blocks = page_dict["blocks"]
        blocks = [item for item in blocks if item["type"] == 0]
        # print(blocks)
        for block in blocks:
            lines = block["lines"]
            for line in lines:
                spans = line["spans"]
                for span in spans:
                    text = span["text"].strip()
                    if text != "" and text != "\x91":
                        page_spans.append(span)
        # print(page_spans)
        for index, span in enumerate(page_spans, start=1):
            if index == 1:
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
                        chapters[current_chapter -
                                 1]['title'] += " " + title
                    else:
                        chapters[current_chapter - 1]['title'] = title
                if size == 20 and font == "Able":
                    if new_chapter_start:
                        chapters[current_chapter -
                                 1]["book_page_number"] = int(text.strip())
                if (size == 13 or size == 11) and (font == "AGaramondPro-Regular" or font == "AGaramondPro-Italic"):
                    x_pos = round(span['origin'][0])
                    if x_pos == new_line_start_x:
                        chapter_text = chapters[current_chapter - 1]['text']
                        if not chapter_text:
                            chapters[current_chapter - 1]['text'] = text
                        else:
                            chapters[current_chapter - 1]['text'] += text

                    else:
                        chapter_text = chapters[current_chapter - 1]['text']
                        if not chapter_text:
                            chapters[current_chapter - 1]['text'] = text
                        else:
                            chapters[current_chapter -
                                     1]['text'] += "\n" + text

    print(len(chapters))
    print(chapters[0]["text"])
