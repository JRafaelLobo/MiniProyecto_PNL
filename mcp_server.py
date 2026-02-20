from typing import Any
from mcp.server.fastmcp import FastMCP

from ingest_pdf import ingest_pdf  
from query_chromadb import search_chromadb

mcp = FastMCP("pdf-tools")

@mcp.tool()
async def ingest_pdf_tool(pdf_path: str) -> str:
    try:
        result = ingest_pdf(pdf_path)
        return f"PDF procesado correctamente: {pdf_path}"
    except Exception as e:
        return f"Error procesando PDF: {str(e)}"

@mcp.tool()
async def search_pdf(query: str, top_k: int = 5) -> Any:
    try:
        results = search_chromadb(query, top_k)
        return results
    except Exception as e:
        return {"error": str(e)}

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()