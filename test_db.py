from query_chromadb import search_chromadb
import chromadb
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DB_PATH = os.path.join(BASE_DIR, "chroma_db")

client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
try:
    col = client.get_collection("pdf_docs")
    print(f"Total de elementos encontrados físicamente: {col.count()}")
except Exception as e:
    print(f"Error: No se encontró la colección. {e}")