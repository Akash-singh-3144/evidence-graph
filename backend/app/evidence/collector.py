import logging

logger = logging.getLogger(__name__)

class EvidenceCollector:
    def __init__(self):
        self.raw_evidence = []

    def collect(self, source_id: str, source_type: str, raw_data: dict, metadata: dict = None):
        """Collects raw output from tools before normalization."""
        item = {
            "source_id": source_id,
            "source_type": source_type,
            "raw_data": raw_data,
            "metadata": metadata or {}
        }
        self.raw_evidence.append(item)
        return item
    
    def get_all(self):
        return self.raw_evidence
