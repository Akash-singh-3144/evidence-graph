import fitz  # PyMuPDF
import logging

logger = logging.getLogger(__name__)

class PDFLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_and_split_by_page(self) -> list[dict]:
        pages_data = []
        try:
            doc = fitz.open(self.file_path)
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                text = page.get_text()
                if text.strip():
                    pages_data.append({
                        "page_number": page_num + 1,
                        "text": text.strip()
                    })
            return pages_data
        except Exception as e:
            logger.error(f"Failed to read PDF {self.file_path}: {str(e)}")
            raise e
