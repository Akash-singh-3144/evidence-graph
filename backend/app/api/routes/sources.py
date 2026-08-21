import os
import uuid
import tempfile
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel
import bs4
import httpx

from app.rag.loaders.pdf_loader import PDFLoader
from app.rag.embeddings.service import EmbeddingService
from app.rag.vectorstore.qdrant_client import VectorStoreClient
from qdrant_client.http.models import VectorParams, Distance

router = APIRouter()

class WebRequest(BaseModel):
    url: str

async def init_qdrant(q_client: VectorStoreClient, size: int = 768):
    try:
        await q_client.client.create_collection(
            collection_name=q_client.collection_name,
            vectors_config=VectorParams(size=size, distance=Distance.COSINE)
        )
    except Exception:
        pass # Already exists

@router.post("/pdf")
async def upload_pdf(file: UploadFile = File(...)):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    content = await file.read()
    temp_file.write(content)
    temp_file.close()

    embedder = EmbeddingService()
    q_client = VectorStoreClient()
    await init_qdrant(q_client, embedder.dimension)

    loader = PDFLoader(temp_file.name)
    pages = loader.load_and_split_by_page()
    source_id = str(uuid.uuid4())
    
    total_chunks = 0
    all_chunks = []
    metadata_map = []
    for page in pages:
        text = page["text"]
        chunks = [text[i:i+800] for i in range(0, len(text), 800)]
        for chunk in chunks:
            if not chunk.strip(): continue
            all_chunks.append(chunk)
            metadata_map.append({"document_name": file.filename, "page_number": page["page_number"]})
            
    if not all_chunks:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="No readable text found in this PDF. Please ensure it contains highlightable text and is not a scanned/image-only document.")

    for i in range(0, len(all_chunks), 90):
        batch_texts = all_chunks[i:i+90]
        batch_meta = metadata_map[i:i+90]
        vectors = await embedder.generate_embeddings_batch(batch_texts)
        for j, vector in enumerate(vectors):
            await q_client.insert_chunk(
                source_id=source_id,
                source_type="pdf",
                text=batch_texts[j],
                vector=vector,
                metadata=batch_meta[j]
            )
        total_chunks += len(batch_texts)

    return {"status": "success", "chunks_indexed": total_chunks}

@router.post("/web")
async def index_web(req: WebRequest):
    embedder = EmbeddingService()
    q_client = VectorStoreClient()
    await init_qdrant(q_client, embedder.dimension)

    async with httpx.AsyncClient() as client:
        resp = await client.get(req.url, follow_redirects=True)
    
    soup = bs4.BeautifulSoup(resp.text, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    
    source_id = str(uuid.uuid4())
    total_chunks = 0
    all_chunks = [text[i:i+800] for i in range(0, len(text), 800)]
    all_chunks = [c for c in all_chunks if c.strip()]
    
    if all_chunks:
        for i in range(0, len(all_chunks), 90):
            batch_texts = all_chunks[i:i+90]
            vectors = await embedder.generate_embeddings_batch(batch_texts)
            for j, vector in enumerate(vectors):
                await q_client.insert_chunk(
                    source_id=source_id,
                    source_type="web",
                    text=batch_texts[j],
                    vector=vector,
                    metadata={"url": req.url, "title": soup.title.string if soup.title else req.url}
                )
            total_chunks += len(batch_texts)
        
    return {"status": "success", "chunks_indexed": total_chunks}

class DBRequest(BaseModel):
    connection_string: str

@router.post("/database")
async def connect_database(req: DBRequest):
    try:
        async with httpx.AsyncClient() as client:
            res = await client.post("http://mcp-db:8003/config", json={"db_url": req.connection_string}, timeout=15.0)
            if res.status_code == 200:
                return {"status": "success"}
            return {"status": "error", "message": res.json().get("detail", "Failed to bind DB.")}
    except Exception as e:
        return {"status": "error", "message": str(e)}
