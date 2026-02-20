import chromadb
import requests

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "pdf_docs"
EMBEDDING_MODEL = "nomic-embed-text"

def embed_query(text):
    r = requests.post(
        "http://localhost:11434/api/embeddings",
        json={"model": EMBEDDING_MODEL, "input": text}
    )
    return r.json()["embedding"]

def search_chromadb(query, top_k=5):
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    col = client.get_collection(COLLECTION_NAME)

    emb = embed_query(query)

    return col.query(
        query_embeddings=[emb],
        n_results=top_k
    )