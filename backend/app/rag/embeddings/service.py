from google import genai
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

_genai_client = None

class EmbeddingService:
    def __init__(self):
        global _genai_client
        if _genai_client is None:
            _genai_client = genai.Client(
                api_key=settings.GEMINI_API_KEY,
                http_options={'api_version': 'v1'}
            )
        self.client = _genai_client
        self.model = settings.EMBEDDING_MODEL
        self.dimension = settings.EMBEDDING_DIMENSION

    async def generate_embeddings_batch(self, texts: list[str]) -> list[list[float]]:
        try:
            embeddings_matrix = []
            for chunk_text in texts:
                try:
                    response = self.client.models.embed_content(
                        model=self.model.strip(),
                        contents=chunk_text
                    )
                except Exception as e:
                    if "NOT_FOUND" in str(e):
                        if self.model.strip() != "embedding-001":
                            logger.warning(f"Model {self.model} not found, falling back to 'embedding-001'")
                            response = self.client.models.embed_content(
                                model="embedding-001",
                                contents=chunk_text
                            )
                        else:
                            raise ValueError("Google API Key explicitly restricts access to all known Embedding models. Please replace your API key with a standard AI Studio key.")
                    else:
                        raise e
                embeddings_matrix.append(response.embeddings[0].values)
            return embeddings_matrix
        except Exception as e:
            logger.error(f"Error generating batch embedding: {str(e)}")
            raise e
