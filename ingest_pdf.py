import os
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
from chromadb import Client
import subprocess
import json
import uuid
import chromadb
import uuid
import requests

CHROMA_DB_PATH = "./chroma_db"
EMBEDDING_MODEL = "nomic-embed-text"
COLLECTION_NAME = "pdf_docs"

def extract_text_and_metadata(pdf_path):
    doc = fitz.open(pdf_path)

    metadata = doc.metadata
    text = ""

    for page in doc:
        text += page.get_text()

    return text, metadata


def chunk_text(text, chunk_size=800, chunk_overlap=150):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

def generate_embedding_ollama(text):
    url = "http://localhost:11434/api/embeddings"
    payload = {
        "model": EMBEDDING_MODEL,
        "prompt": text
    }

    response = requests.post(url, json=payload)

    if response.status_code != 200:
        raise RuntimeError(f"Error de Ollama: {response.text}")

    data = response.json()
    return data["embedding"]


def store_in_chromadb(chunks, metadata, pdf_name):
    client = chromadb.PersistentClient(path=CHROMA_DB_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
        embedding_function=None
    )

    for chunk in chunks:
        emb = generate_embedding_ollama(chunk)

        collection.add(
            ids=[str(uuid.uuid4())],
            metadatas=[{
                "source_pdf": pdf_name,
                "pdf_metadata":  json.dumps(metadata, ensure_ascii=False)
            }],
            documents=[chunk],
            embeddings=[emb]
        )


def ingest_pdf(pdf_path = './Documentos/CobiT4_Espanol.pdf'):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"No se encontró el PDF: {pdf_path}")
    text, metadata = extract_text_and_metadata(pdf_path)
    chunks = chunk_text(text)
    store_in_chromadb(chunks, metadata, os.path.basename(pdf_path))