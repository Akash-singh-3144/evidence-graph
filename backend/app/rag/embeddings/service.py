from app.config.settings import settings
import logging
import httpx

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.EMBEDDING_MODEL.strip()
        if not self.model.startswith("models/"):
            self.model = f"models/{self.model}"
        self.dimension = settings.EMBEDDING_DIMENSION

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        # Using raw httpx REST proxy to flawlessly authenticate without relying on the python SDK version restrictions
        url = f"https://generativelanguage.googleapis.com/v1beta/{self.model}:embedContent?key={self.api_key}"
        embeddings_matrix = []
        
        async with httpx.AsyncClient(timeout=45.0) as client:
            for chunk_text in texts:
                payload = {
                    "model": self.model,
                    "content": {
                        "parts": [{"text": chunk_text}]
                    }
                }
                response = await client.post(url, json=payload)
                
                if response.status_code != 200:
                    error_data = response.text
                    logger.error(f"Google REST API Error: {response.status_code} - {error_data}")
                    raise ValueError(f"Google Embedding API rejected the request: HTTP {response.status_code}. Detail: {error_data}")
                
                res_json = response.json()
                try:
                    emb_values = res_json["embedding"]["values"]
                    embeddings_matrix.append(emb_values)
                except KeyError:
                    raise ValueError(f"Failed to parse embedding vectors from valid REST response: {res_json}")
                    
        return embeddings_matrix
