import chromadb
import os
import ollama 


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DB_PATH = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "pdf_docs"
EMBEDDING_MODEL = "mxbai-embed-large"

def embed_query(text):
    try:
        response = ollama.embed(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response['embeddings'][0]
    except Exception as e:
        print(f"Error al generar embedding de búsqueda: {e}")
        return None

def search_chromadb(query, top_k=5):
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
    
    try:
        col = client.get_collection(COLLECTION_NAME)
    except Exception:
        return {"error": "No se encontró la colección. ¿Ya corriste la ingesta?"}
    
    if col.count() == 0:
        return {"error": "La base de datos está vacía. Ingiere el PDF de nuevo."}

    emb = embed_query(query)
    
    if emb is None:
        return {"error": "No se pudo generar el vector para la consulta."}

    results = col.query(
        query_embeddings=[emb],
        n_results=top_k
    )
    
    return results