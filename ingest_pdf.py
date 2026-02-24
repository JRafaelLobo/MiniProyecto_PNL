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
            print(f" Error en trozo {i}: {e}")

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


def ingest_pdf(folder_path='./Documentos'):
    pdf_files = glob.glob(os.path.join(folder_path, "*.pdf"))
    
    if not pdf_files:
        print(f"No se encontraron archivos PDF en la carpeta: {folder_path}")
        return

    print(f"Se encontraron {len(pdf_files)} archivos para procesar.")

    for pdf_path in pdf_files:
        pdf_name = os.path.basename(pdf_path)
        print(f"\n--- Procesando: {pdf_name} ---")
        
        try:
            text, metadata = extract_text_and_metadata(pdf_path)
            
            if len(text) < 10:
                print(f"Saltando {pdf_name}: No tiene texto extraíble.")
                continue
            
           
            chunks = chunk_text(text)
            print(f"Texto limpio y dividido en {len(chunks)} trozos.")

            store_in_chromadb(chunks, metadata, pdf_name)
            
        except Exception as e:
            print(f"Error procesando {pdf_name}: {e}")
