from embeddings import return_similarity_scores, calculate_embeddings
from chat import Chat
from data import Data
from assistant import Assistant

assistant1 = Assistant(Data.assistants[1], Data.user_info)
chat1 = Chat(Data.user_info,
             assistant1, "assistant", Data.assistant_chat_params, 0)


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
query = "Who is referred to as 'the woman' by Sherlock Holmes?"
# chunks_embeddings = calculate_embeddings("array", chunks, "sherlock-holmes-2")
similarity = return_similarity_scores(
    chunks, "json", "./week-3/chatbot-cmd-class/data/sherlock-holmes-2.json", query, 5)
# print(similarity_texts)
print(query)
answer = chat1.generate_output(query, similarity)
print(answer)
