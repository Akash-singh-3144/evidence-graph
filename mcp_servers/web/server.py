from fastapi import FastAPI

app = FastAPI(title="Web MCP Server")

@app.get("/search")
async def search_web(query: str) -> str:
    return f"Simulated Web Search for {query}"

@app.get("/fetch")
async def fetch_webpage(url: str) -> str:
    return f"Simulated content extracted from {url}"
