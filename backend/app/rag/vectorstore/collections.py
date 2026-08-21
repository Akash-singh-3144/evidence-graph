from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import Distance, VectorParams
from app.config.settings import settings

client = AsyncQdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT)

EVIDENCE_COLLECTION = "evidence_chunks"

async def init_qdrant():
    collections = await client.get_collections()
    collection_names = [c.name for c in collections.collections]

    if EVIDENCE_COLLECTION not in collection_names:
        await client.create_collection(
            collection_name=EVIDENCE_COLLECTION,
            vectors_config=VectorParams(
                size=settings.EMBEDDING_DIMENSION,
                distance=Distance.COSINE
            )
        )
