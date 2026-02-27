import logging
import chromadb
import os
import ollama 

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(BASE_DIR, "server_query.log")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE_PATH), 
        logging.StreamHandler()             
    ]
)
logger = logging.getLogger(__name__)

CHROMA_DB_PATH = os.path.join(BASE_DIR, "chroma_db")
COLLECTION_NAME = "pdf_docs"
EMBEDDING_MODEL = "mxbai-embed-large"


def embed_query(text):
    try:
        logger.info(f"Generando embedding para la consulta: '{text[:50]}...'")
        response = ollama.embed(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response['embeddings'][0]
    except Exception as e:
        logger.error(f"Fallo crítico en Ollama (Search): {e}")
        return None

def search_chromadb(query, top_k=5):
    logger.info(f"Nueva búsqueda recibida de Claude: '{query}'")
    
    try:
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        col = client.get_collection(COLLECTION_NAME)
    except Exception as e:
        logger.critical(f"No se pudo acceder a ChromaDB: {e}")
        return {"error": "No se encontró la colección. ¿Ya corriste la ingesta?"}
    
    total_docs = col.count()
    if total_docs == 0:
        logger.warning("La colección existe pero está vacía.")
        return {"error": "La base de datos está vacía. Ingiere el PDF de nuevo."}

    emb = embed_query(query)
    
    if emb is None:
        return {"error": "No se pudo generar el vector para la consulta."}

    try:
        logger.info(f"Buscando en {total_docs} vectores...")
        results = col.query(
            query_embeddings=[emb],
            n_results=top_k
        )
        
        # Log para saber cuántos resultados relevantes encontramos
        num_results = len(results.get('documents', [[]])[0])
        logger.info(f"Búsqueda completada. Se encontraron {num_results} fragmentos relevantes.")
        
        return results
    except Exception as e:
        logger.error(f"Error durante la ejecución de la consulta en ChromaDB: {e}")
        return {"error": "Error interno al consultar la base de datos."}