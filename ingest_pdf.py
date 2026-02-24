import os
import fitz
import json
import uuid
import requests
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
import ollama

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DB_PATH = os.path.join(BASE_DIR, "chroma_db")
EMBEDDING_MODEL = "mxbai-embed-large"
COLLECTION_NAME = "pdf_docs"


def extract_text_and_metadata(pdf_path):
    doc = fitz.open(pdf_path)
    metadata = doc.metadata
    text = "\n".join([page.get_text() for page in doc])
    return text, metadata

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
        print(f"Error generando embedding con Ollama: {e}")
        return None

def store_in_chromadb(chunks, metadata, pdf_name):
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
            
            if i % 5 == 0:
                print(f"   Procesados {i}/{len(chunks)}...")
        except Exception as e:
            print(f"   Error en trozo {i}: {e}")

    if not all_ids:
        print("ERROR: No se generó ningún embedding. ¿Ollama está corriendo?")
        return

    collection.add(
        ids=all_ids,
        embeddings=all_embeddings,
        metadatas=all_metadatas,
        documents=all_documents
    )
    print(f"¡ÉXITO! Se guardaron {len(all_ids)} elementos en ChromaDB.")

def ingest_pdf(pdf_path='./Documentos/CobiT4_Espanol.pdf'):
    if not os.path.exists(pdf_path):
        print(f"ERROR: El archivo no existe en {pdf_path}")
        return

    print(f"--- Iniciando diagnóstico ---")
    text, metadata = extract_text_and_metadata(pdf_path)
    
    print(f"1. Caracteres extraídos del PDF: {len(text)}")
    if len(text) < 10:
        print("ERROR: El PDF no tiene texto extraíble. ¿Es una imagen escaneada?")
        return

    chunks = chunk_text(text)
    print(f"2. Número de trozos (chunks) creados: {len(chunks)}")
    store_in_chromadb(chunks, metadata, os.path.basename(pdf_path))