from app.rag.embeddings.service import EmbeddingService
from app.rag.vectorstore.qdrant_client import VectorStoreClient
import logging

logger = logging.getLogger(__name__)

class Retriever:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.vector_store = VectorStoreClient()

    async def retrieve(self, query: str, source_type: str = None, limit: int = 5):
        try:
            query_vector = await self.embedding_service.generate_embedding(query)
            results = await self.vector_store.search(
                vector=query_vector,
                source_type=source_type,
                limit=limit
            )
            
            # Format results
            retrieved = []
            for res in results:
                retrieved.append({
                    "id": res.id,
                    "score": res.score,
                    "payload": res.payload
                })
            return retrieved
        except Exception as e:
            logger.error(f"Retrieval failed: {str(e)}")
            raise e
