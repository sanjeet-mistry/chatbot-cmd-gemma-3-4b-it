from embeddings_old import return_similarity_scores
# query = "I got a new mobile number. How to update?"
query = "What time does Swapnil have dinner at?"
results = return_similarity_scores(
    "text", "./week-3/chatbot-cmd-class/data/info.txt", query, 5)
# results = return_similarity_scores(
#     "json", "./week-3/chatbot-cmd-class/data/laptops.json", query, 3)
# results = return_similarity_scores(
#     "chat", "./week-3/chatbot-cmd-class/chats/chat-49107931.txt", query, 3)
print(f"Query: {query}")
for i in range(len(results)):
    print(f"{i+1}. {results[i]['text']} ({results[i]['similarity']})")
