import httpx
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class WebLoader:
    def __init__(self, url: str):
        self.url = url

    async def load(self) -> str:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(self.url, timeout=10.0)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Remove scripts and styles
                for script in soup(["script", "style"]):
                    script.extract()
                    
                text = soup.get_text(separator=' ', strip=True)
                return text
        except Exception as e:
            logger.error(f"Failed to fetch Web {self.url}: {str(e)}")
            raise e
