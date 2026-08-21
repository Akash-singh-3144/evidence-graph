from qdrant_client import AsyncQdrantClient
from qdrant_client.http.models import PointStruct, Filter, FieldCondition, MatchValue
from app.config.settings import settings
import uuid
import datetime

_qdrant_client = None

class VectorStoreClient:
    def __init__(self):
        global _qdrant_client
        if _qdrant_client is None:
            if settings.QDRANT_HOST.endswith(".onrender.com"):
                # Force public HTTPS routing to physically wake up the sleeping Free Tier Qdrant node
                _qdrant_client = AsyncQdrantClient(url=f"https://{settings.QDRANT_HOST}", port=443, timeout=45.0)
            elif settings.QDRANT_HOST.startswith("http"):
                _qdrant_client = AsyncQdrantClient(url=settings.QDRANT_HOST, timeout=45.0)
            else:
                _qdrant_client = AsyncQdrantClient(host=settings.QDRANT_HOST, port=settings.QDRANT_PORT, timeout=45.0)
        self.client = _qdrant_client
        self.collection_name = "evidence_chunks"

    async def insert_chunk(self, source_id: str, source_type: str, text: str, vector: list[float], metadata: dict):
        point_id = str(uuid.uuid4())
        payload = {
            "source_id": source_id,
            "source_type": source_type,
            "text": text,
            "indexed_at": datetime.datetime.utcnow().isoformat(),
            **metadata
        }

        await self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=payload
                )
            ]
        )
        return point_id

    async def search(self, vector: list[float], source_type: str = None, limit: int = 5):
        query_filter = None
        if source_type:
            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="source_type",
                        match=MatchValue(value=source_type)
                    )
                ]
            )

        response = await self.client.query_points(
            collection_name=self.collection_name,
            query=vector,
            query_filter=query_filter,
            limit=limit
        )
        return response.points
