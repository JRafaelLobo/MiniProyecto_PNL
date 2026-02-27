import logging
import os
import fitz
import json
import uuid
import requests
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
import ollama
import glob 

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE_PATH = os.path.join(BASE_DIR, "ingestion.log")
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
EMBEDDING_MODEL = "mxbai-embed-large"
COLLECTION_NAME = "pdf_docs"

def extract_text_and_metadata(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        metadata = doc.metadata
        text = "\n".join([page.get_text() for page in doc])
        return text, metadata
    except Exception as e:
        logger.error(f"Error al abrir el PDF {pdf_path}: {e}")
        raise

def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )
    return splitter.split_text(text)

def generate_embedding_ollama(text):
    try:
        response = ollama.embed(
            model=EMBEDDING_MODEL,
            input=text
        )
        return response['embeddings'][0]
    except Exception as e:
        logger.error(f"Fallo en Ollama al generar embedding: {e}")
        return None

def store_in_chromadb(chunks, metadata, pdf_name):
    try:
        client = chromadb.PersistentClient(path=CHROMA_DB_PATH)
        collection = client.get_or_create_collection(COLLECTION_NAME)

        all_ids, all_embeddings, all_metadatas, all_documents = [], [], [], []

        for i, chunk in enumerate(chunks):
            try:
                emb = generate_embedding_ollama(chunk)
                if emb:
                    all_ids.append(str(uuid.uuid4()))
                    all_embeddings.append(emb)
                    all_metadatas.append({"source_pdf": pdf_name})
                    all_documents.append(chunk)
                
                if i % 10 == 0:
                    logger.info(f"   [{pdf_name}] Procesados {i}/{len(chunks)} trozos...")
            except Exception as e:
                logger.warning(f" Error en trozo {i} del PDF {pdf_name}: {e}")

        if not all_ids:
            logger.error(f"No se generaron embeddings para {pdf_name}. Verifica Ollama.")
            return

        collection.add(
            ids=all_ids,
            embeddings=all_embeddings,
            metadatas=all_metadatas,
            documents=all_documents
        )
        logger.info(f"¡ÉXITO! {pdf_name} guardado con {len(all_ids)} vectores.")
    except Exception as e:
        logger.critical(f"Fallo crítico al guardar en ChromaDB: {e}")

def ingest_pdf(folder_path='./Documentos'):
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    
    if not pdf_files:
        logger.warning(f"Carpeta vacía o sin PDFs: {folder_path}")
        return

    logger.info(f"Iniciando ingesta masiva: {len(pdf_files)} archivos encontrados.")

    for pdf_path in pdf_files:
        pdf_name = os.path.basename(pdf_path)
        logger.info(f"--- PROCESANDO: {pdf_name} ---")
        
        try:
            text, metadata = extract_text_and_metadata(pdf_path)
            
            if len(text) < 10:
                logger.warning(f"PDF sin contenido legible: {pdf_name}")
                continue
            
            chunks = chunk_text(text)
            logger.info(f"Dividido en {len(chunks)} trozos.")
            store_in_chromadb(chunks, metadata, pdf_name)
            
        except Exception as e:
            logger.error(f"Error fatal procesando {pdf_name}: {e}")

if __name__ == "__main__":
    ingest_pdf()
