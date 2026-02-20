
# 🧠 MiniProyecto de PLN – MCP Server + RAG Pipeline

Este proyecto implementa un **MCP Server en Python** capaz de:
- Extraer texto desde documentos PDF.
- Realizar *chunking* del contenido.
- Generar **embeddings** usando **Ollama**.
- Almacenar texto y vectores en **ChromaDB**.
- Permitir búsqueda semántica.
- Ser orquestado desde **Claude Desktop**.

El objetivo es construir un pipeline funcional de **RAG (Retrieval Augmented Generation)** usando herramientas locales y eficientes.

## 📦 Arquitectura General
**Claude Desktop** → **MCP Server (Python)** → Ingestión PDF → Chunking → Embeddings (Ollama) → ChromaDB → Búsqueda → Respuesta.

## 🛠 Tecnologías utilizadas
- Python
- PyMuPDF / LangChain
- Ollama
- ChromaDB
- Claude Desktop

## 📘 Pipeline RAG
1. Cargar PDF.
2. Extraer texto.
3. Chunking.
4. Embeddings con Ollama.
5. Guardar datos en ChromaDB.
6. Búsqueda semántica.
7. Respuesta hacia Claude.

## 📑 Instalación
```
pip install -r requirements.txt
```
Requisitos sugeridos:
```
chromadb
pymupdf
langchain
langchain-community
python-dotenv
requests
```
Instalar Ollama:
https://ollama.com/download

Descargar embedding model:
```
ollama pull nomic-embed-text
```

## 🚀 SetUpRapido

```bash
./setup.sh
```

## ⚡ Ejecutar

```bash
./start.sh
```

## 📁 Estructura del Proyecto
```
.
├── Documentos                     # PDFs y material de referencia
│   └── CobiT4_Espanol.pdf         # Documento base del proyecto
├── README.md                      # Documentación principal
├── TestingFiles                   # Área de pruebas, prototipos y versiones previas
├── chroma_db                      # Base de datos principal del proyecto
├── ingest_pdf.py                  # Ingesta del PDF a vectores
├── mcp_server.py                  # Servidor MCP del proyecto
├── query_chromadb.py              # Consultas a la base vectorial
├── requirements.txt               # Dependencias globales del proyecto
├── setup.sh                       # Script de instalación / setup principal
└── start.sh                       # Script para iniciar el sistema
```

## 🎯 Requisitos del proyecto
- Extraer texto PDF
- Chunking
- Embeddings en Ollama
- ChromaDB
- Búsqueda semántica
- MCP Server
- Integración con Claude Desktop


## 👥 Autores

| Nombre | Contacto |
|--------|-----------|
| **José Lobo** | https://github.com/JRafaelLobo |
| **Marcela Tovar**  | https://github.com/MarcelaTovar |