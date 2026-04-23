calculate_embedding = False
calculate_similarity = True
file_name = "sherlock-holmes-e5-base-v2"


def chunk_text(text, chunk_size=200):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))

    return chunks


def chunk_text_overlap(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size - overlap):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))

    return chunks


with open("./week-3/chatbot-cmd-class/data/sherlock-holmes.txt", encoding='utf-8') as f:
    text = f.read()
chunks = chunk_text_overlap(text)
# Basic comprehension questions
queries = [
    "Who is referred to as “the woman” by Sherlock Holmes?",
    "What is the name of Holmes’s close friend and narrator of the story?",
    "Why had Holmes and Watson seen little of each other lately?",
    "What street does Holmes live on?",
    "What habit of Holmes is mentioned involving cocaine and ambition?"
]
# Observation & deduction questions
# queries = [
#     "How does Holmes deduce that Watson had been out in bad weather?",
#     "What clues does Holmes use to conclude that Watson is back in medical practice?",
#     "According to Holmes, what is the difference between “seeing” and “observing”?",
#     "How many steps lead up to Holmes’s room?"
# ]
# Mystery & plot questions
# queries = [
#     "At what time is the mysterious visitor supposed to arrive?",
#     "What unusual request does the note make about the visitor’s appearance?",
#     "From which region does Holmes deduce the paper of the letter comes?",
#     "What title does the visitor initially give himself?",
#     "Who does the visitor later reveal himself to be?"
# ]
# Irene Adler & case details
# queries = [
#     "Who is Irene Adler, and why is she important to the case?",
#     "What does the King want Holmes to recover?",
#     "Why is the photograph dangerous to the King?",
#     "Where does Irene Adler live?"
# ]
# Later events
# queries = [
#     "What disguise does Holmes use to investigate Irene Adler?",
#     "What trick does Holmes use to find where the photograph is hidden?",
#     "What happens to Irene Adler at the end of the story?",
#     "Why does Holmes ultimately fail to obtain the photograph?"
# ]
if calculate_embedding:
    from embeddings import calculate_embeddings
    chunks_embeddings = calculate_embeddings(
        "array", chunks, file_name)
elif calculate_similarity:
    from embeddings import return_similarity_scores
    similarity_scores = []
    for query in queries:
        similarity_scores.append(return_similarity_scores(
            chunks, "json", f"./week-3/chatbot-cmd-class/data/{file_name}.json", query, 4))

    from data import Data
    from assistant import Assistant
    assistant1 = Assistant(Data.assistants[3], Data.user_info)
    from chat import Chat
    chat1 = Chat(Data.user_info,
                 assistant1, "assistant", Data.assistant_chat_params, 0)
    for i in range(len(similarity_scores)):
        print(queries[i])
        answer = chat1.generate_output(queries[i], similarity_scores[i])
        print(f"{answer}\n")
