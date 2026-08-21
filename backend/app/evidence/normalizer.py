import uuid
import datetime
import logging

logger = logging.getLogger(__name__)

class EvidenceNormalizer:
    @staticmethod
    def normalize(raw_item: dict) -> dict:
        """
        Normalizes any tool output into the common evidence schema.
        {
          "evidence_id": "uuid",
          "source_id": "uuid",
          "source_type": "pdf | web | database",
          "content": "...",
          "claim": "...",
          "retrieved_at": "...",
          ...
        }
        """
        source_type = raw_item.get("source_type")
        raw_data = raw_item.get("raw_data", {})
        metadata = raw_item.get("metadata", {})

        normalized = {
            "evidence_id": str(uuid.uuid4()),
            "source_id": raw_item.get("source_id"),
            "source_type": source_type,
            "source_name": metadata.get("source_name", "Unknown"),
            "content": "",
            "claim": metadata.get("claim", ""),
            "retrieval_score": metadata.get("score", 1.0),
            "retrieved_at": datetime.datetime.utcnow().isoformat(),
            "authority": "medium",
            "freshness": "medium",
            "citation": {}
        }

        if source_type == "database":
            normalized["content"] = str(raw_data)
            normalized["raw_data_passthrough"] = raw_data
            normalized["authority"] = "high"
            normalized["citation"] = {"query": metadata.get("query")}
        elif source_type in ["pdf", "web"]:
            normalized["content"] = raw_data.get("text", "")
            normalized["citation"] = {"page": metadata.get("page"), "url": metadata.get("url")}
        
        return normalized
