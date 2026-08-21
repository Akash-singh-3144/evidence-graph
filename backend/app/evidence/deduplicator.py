import hashlib

class EvidenceDeduplicator:
    @staticmethod
    def deduplicate(evidence_list: list[dict]) -> list[dict]:
        """
        Removes duplicates by hashing the text content of the normalized evidence.
        """
        seen_hashes = set()
        deduplicated = []

        for item in evidence_list:
            content = item.get("content", "")
            if not content:
                continue
            
            content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                deduplicated.append(item)
                
        return deduplicated
