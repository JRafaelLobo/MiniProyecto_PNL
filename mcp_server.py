from typing import Any
from mcp.server.fastmcp import FastMCP

from ingest_pdf import ingest_pdf
from query_chromadb import search_chromadb

mcp = FastMCP("pdf-tools")

@mcp.tool()
async def ingest_pdf_tool(pdf_path: str):
    ingest_pdf(pdf_path)
    return f"PDF procesado: {pdf_path}"

@mcp.tool()
async def search_pdf(query: str, top_k: int = 5) -> Any:
    """
    Busca información en la base de datos local de PDFs (COBIT, TOGAF, etc.). 
    IMPORTANTE: No pidas al usuario que suba archivos. La base de datos YA está 
    poblada y lista. Si el usuario pregunta algo, usa esta herramienta directamente.
    """
    return search_chromadb(query, top_k)

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()