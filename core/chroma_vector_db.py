import chromadb


class ChromaVectorDB():
    def create_collection(self, chunks, embeddings_array, collection_path, collection_name):
        self.collection_name = collection_name
        self.collection_path = collection_path
        client = chromadb.PersistentClient(path=collection_path)
        collection = client.get_or_create_collection(
            name=collection_name)

        for i, doc in enumerate(chunks):
            collection.add(
                documents=[doc],
                embeddings=[embeddings_array[i]],
                ids=[str(i)]
            )

    def return_best_results(self, collection_name, collection_path, queries=None, num_of_results=20, use_reranker=True, top_k={'min': 2, 'max': 10}):
        from core.embeddings_old import calculate_embeddings
        client = chromadb.PersistentClient(path=collection_path)
        collection = client.get_or_create_collection(
            name=collection_name)
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
                n_results=num_of_results
            )

            docs = results["documents"][0]

            if not use_reranker:
                top_chunks.append(docs)
            else:
                pairs = [[query, doc] for doc in docs]

                # Step 3: Rerank
                scores = reranker.predict(pairs)

                # Step 4: Sort by score
                ranked_docs = sorted(
                    zip(docs, scores), key=lambda x: x[1], reverse=True)

                top_doc = ranked_docs[0]
                top_docs = [(doc, score) for doc,
                            score in ranked_docs if score >= max((.35 * top_doc[1]), .15)]

                if len(top_docs) < top_k['min']:
                    top_docs = ranked_docs[:top_k['min']]
                elif len(top_docs) > top_k['max']:
                    top_docs = top_docs[:top_k['max']]

                print([score for doc, score in top_docs])
                top_docs = [doc for doc, score in top_docs]

                top_chunks.append(top_docs)

        return top_chunks
