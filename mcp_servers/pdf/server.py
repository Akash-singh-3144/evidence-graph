from fastapi import FastAPI

app = FastAPI(title="PDF MCP Server")

@app.get("/search")
async def search_documents(query: str, limit: int = 5) -> str:
    return f"Simulated PDF search for {query}"

@app.get("/chunk")
async def get_document_chunk(chunk_id: str) -> str:
    return f"Simulated PDF chunk retrieval for {chunk_id}"
