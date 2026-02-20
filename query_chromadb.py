import chromadb

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "pdf_docs"

def search_chromadb(query: str, top_k: int = 5):
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    collection = client.get_collection(COLLECTION_NAME)

    results = collection.query(
        query_texts=[query],
        n_results=top_k
    )

    return results