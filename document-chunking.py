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


with open("./week-3/chatbot-cmd-class/data/sherlock-holmes.txt", encoding='utf-8') as f:
    text = f.read()
chunks = chunk_text(text)
queries = [
    "What is the name of Holmes’s close friend and narrator of the story?",
    "What street does Holmes live on?",
    "How many steps lead up to Holmes’s room?",
    "How does Holmes deduce that Watson had been out in bad weather?",
    "At what time is the mysterious visitor supposed to arrive?",
    "From which region does Holmes deduce the paper of the letter comes?",
    "What disguise does Holmes use to investigate Irene Adler?",
    "What does the King want Holmes to recover?",
    "What trick does Holmes use to find where the photograph is hidden?",
    "Why does Holmes ultimately fail to obtain the photograph?"
]
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
