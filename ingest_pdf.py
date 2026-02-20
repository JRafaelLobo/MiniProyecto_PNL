import os
import fitz
import json
import uuid
import requests
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHROMA_DB_PATH = "./chroma_db"
COLLECTION_NAME = "pdf_docs"
EMBEDDING_MODEL = "nomic-embed-text"

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
    url = "http://localhost:11434/api/embeddings"
    payload = {"model": EMBEDDING_MODEL, "input": text}

    r = requests.post(url, json=payload)
    if r.status_code != 200:
        raise RuntimeError(f"Ollama error: {r.text}")

    return r.json()["embedding"]

def store_in_chromadb(chunks, metadata, pdf_name):
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    collection = client.get_or_create_collection(
        COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"}
    )

    for chunk in chunks:
        emb = generate_embedding_ollama(chunk)

        collection.add(
            ids=[str(uuid.uuid4())],
            metadatas=[{
                "source_pdf": pdf_name
            }],
            documents=[chunk],
            embeddings=[emb]
        )

def ingest_pdf(pdf_path='./Documentos/CobiT4_Espanol.pdf'):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"No se encontró: {pdf_path}")

    text, metadata = extract_text_and_metadata(pdf_path)
    chunks = chunk_text(text)
    store_in_chromadb(chunks, metadata, os.path.basename(pdf_path))