from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(logs):
    texts = [log["raw"] for log in logs]
    embeddings = model.encode(texts)
    return embeddings