import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection("spi_logs")

def store_embeddings(logs, embeddings):
    for i, (log, emb) in enumerate(zip(logs, embeddings)):
        collection.add(
            embeddings=[emb],
            documents=[log["raw"]],
            ids=[str(i)]
        )

def retrieve_similar(query_embedding):
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=2
    )
    return results["documents"]