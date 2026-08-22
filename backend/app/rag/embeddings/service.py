from google import genai
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

_genai_client = None

class EmbeddingService:
    def __init__(self):
        global _genai_client
        if _genai_client is None:
            _genai_client = genai.Client(api_key=settings.GEMINI_API_KEY)
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
                        logger.warning(f"Model {self.model} not found, falling back to 'text-embedding-004'")
                        response = self.client.models.embed_content(
                            model="text-embedding-004",
                            contents=chunk_text
                        )
                    else:
                        raise e
                embeddings_matrix.append(response.embeddings[0].values)
            return embeddings_matrix
        except Exception as e:
            logger.error(f"Error generating batch embedding: {str(e)}")
            raise e
