import chromadb


class ChromaVectorDB():
    show_console_logs = True

    def __init__(self, collection_name, collection_path):
        self.collection_name = collection_name
        self.collection_path = collection_path

    def create_collection(self, document_metadata, chunks, embeddings_array):
        client = chromadb.PersistentClient(path=self.collection_path)
        collection = client.get_or_create_collection(
            name=self.collection_name,
            metadata={
                "source": document_metadata["source"],
                "title": document_metadata["title"],
                "series": document_metadata["series"],
                "book_number": document_metadata["book_number"],
                "author": document_metadata["author"],
                "category": document_metadata["category"],
                "language": document_metadata["language"],
                "publication_year": document_metadata["publication_year"],
                "universe": document_metadata["universe"]
            })
        chunks_text = [chunk["text"] for chunk in chunks]

        for i, doc in enumerate(chunks):
            collection.add(
                documents=[chunks_text[i]],
                embeddings=[embeddings_array[i]],
                ids=[str(i)],
                metadatas=[
                    {
                        "pdf-page": doc["pdf-page"],
                        "book-page": doc["book-page"],
                        "chapter-number": doc["chapter-number"],
                        "chapter-title": doc["chapter-title"],

                        "chunk_id": i,
                        "chunk_index": i,
                    }
                ]
            )

    def return_best_results(self, queries=None, num_of_results=20, use_reranker=True, top_k={'min': 2, 'max': 10}):
        from core.embeddings_old import calculate_embeddings
        client = chromadb.PersistentClient(path=self.collection_path)
        collection = client.get_or_create_collection(
            name=self.collection_name)
        top_chunks = []
        if isinstance(queries, str):
            queries = [queries]

        if use_reranker:
            from sentence_transformers import CrossEncoder
            reranker = CrossEncoder("./models/bge-reranker-base")

        for query in queries:
            query_embedding = calculate_embeddings("string", query)
            results = collection.query(
                query_embeddings=query_embedding,
                n_results=num_of_results,
                include=["documents", "distances", "metadatas"]
            )

            docs = results["documents"][0]
            ids = results["ids"][0]
            distances = results["distances"][0]
            metadatas = results["metadatas"][0]

            if ChromaVectorDB.show_console_logs:
                for doc, distance in zip(docs, distances):
                    print(doc)
                    print(f"Distance: {distance}")
                print()

            if not use_reranker:
                top_chunks.append(docs)
            else:
                pairs = [[query, doc] for doc in docs]

                # Step 3: Rerank
                scores = reranker.predict(pairs)

                # Step 4: Sort by score
                ranked_docs = sorted(
                    zip(docs, distances, metadatas, scores), key=lambda x: x[3], reverse=True)

                top_doc = ranked_docs[0]
                top_score = top_doc[3]
                if top_score >= .15:
                    top_docs = [(doc, distance, metadata, score) for doc, distance, metadata,
                                score in ranked_docs if score >= (.35 * top_score)]

                    if len(top_docs) < top_k['min']:
                        if top_score >= .3:
                            top_docs = ranked_docs[:top_k['min']]
                        else:
                            top_docs = ranked_docs[:top_k['max']]
                    elif len(top_docs) > top_k['max']:
                        top_docs = ranked_docs[:top_k['max']]
                else:
                    top_docs = ranked_docs[:top_k['max']]

                if ChromaVectorDB.show_console_logs:
                    print("Reranker chunks:")
                    for top_doc in top_docs:
                        print(top_doc[0])
                        print(f"Score: {top_doc[3]}")

                top_docs = [doc for doc, distance, metadata,
                            score in top_docs]
                top_chunks.append(top_docs)

        return top_chunks
