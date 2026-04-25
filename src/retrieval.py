import chromadb
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "db")

# Persistent client — survives between runs
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection("spi_logs")


def clear_collection():
    """Clear all stored embeddings (useful for re-indexing)."""
    global collection
    client.delete_collection("spi_logs")
    collection = client.get_or_create_collection("spi_logs")


def store_embeddings(logs, embeddings, id_prefix="kb"):
    """
    Store logs + embeddings into ChromaDB.
    id_prefix: use 'kb' for knowledge base, 'query' for runtime logs.
    """
    existing_ids = set(collection.get()["ids"])
    new_logs, new_embs, new_ids, new_metas = [], [], [], []

    for i, (log, emb) in enumerate(zip(logs, embeddings)):
        uid = f"{id_prefix}_{i}"
        if uid in existing_ids:
            continue  # Skip duplicates
        new_logs.append(log["raw"])
        new_embs.append(emb.tolist())
        new_ids.append(uid)
        new_metas.append({"status": log["status"]})

    if new_logs:
        collection.add(
            embeddings=new_embs,
            documents=new_logs,
            metadatas=new_metas,
            ids=new_ids
        )
        print(f"Stored {len(new_logs)} new entries with prefix '{id_prefix}'.")
    else:
        print("No new entries to store (all already in DB).")


def retrieve_similar(query_embedding, n_results=3, exclude_ids=None):
    """
    Retrieve similar logs from the knowledge base.
    exclude_ids: list of IDs to exclude (to avoid self-retrieval).
    """
    total = collection.count()
    if total == 0:
        return []

    fetch_n = min(n_results + len(exclude_ids or []), total)
    results = collection.query(
        query_embeddings=[query_embedding.tolist()],
        n_results=fetch_n
    )

    docs = results["documents"][0]
    ids = results["ids"][0]

    # Filter out self-matches
    filtered = [
        doc for doc, rid in zip(docs, ids)
        if exclude_ids is None or rid not in exclude_ids
    ]
    return filtered[:n_results]
