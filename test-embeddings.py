from embeddings import Embeddings
emd1 = Embeddings()
query = "I got a new mobile number. How to update?"
results = emd1.return_similarity_scores(
    "./week-3/embeddings/faq.txt", None, query, 3)
print(f"Query: {query}")
for i in range(len(results)):
    print(f"{i+1}. {results[i]["text"]} ({results[i]["similarity"]})")
