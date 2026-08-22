from app.config.settings import settings
import logging
import httpx

logger = logging.getLogger(__name__)

class EmbeddingService:
    def __init__(self):
        # We are completely bypassing Google embeddings to circumvent geographic / billing blockades.
        # We enforce a massive 768-dimensional model standard to match the Qdrant DB schema natively.
        self.huggingface_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-mpnet-base-v2"
        self.dimension = 768

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        embeddings_matrix = []
        
        async with httpx.AsyncClient(timeout=45.0) as client:
            # Send the entire batch array strictly as 1 HTTP request to preserve free HF rate limits
            payload = {"inputs": texts}
            response = await client.post(self.huggingface_url, json=payload)
            
            if response.status_code != 200:
                error_data = response.text
                logger.error(f"HuggingFace REST API Error: {response.status_code} - {error_data}")
                
                if "loading" in error_data.lower():
                    raise ValueError(f"HuggingFace cold-start: Model is currently loading into memory. Please wait exactly 30 seconds and click Upload again! {error_data}")
                raise ValueError(f"HuggingFace Embedding API rejected the request: HTTP {response.status_code}. Detail: {error_data}")
            
            res_json = response.json()
            if isinstance(res_json, list) and len(res_json) > 0 and isinstance(res_json[0], list):
                # The pipeline directly returns the multidimensional float matrix
                return res_json
            else:
                raise ValueError(f"Failed to parse embedding vectors from HuggingFace response: {res_json[:100]}")
