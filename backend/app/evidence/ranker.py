class EvidenceRanker:
    @staticmethod
    def rank(evidence_list: list[dict]) -> list[dict]:
        """
        Ranks normalized evidence based on retrieval_score and authority.
        """
        def get_authority_score(authority: str) -> float:
            scores = {"high": 1.0, "medium": 0.5, "low": 0.2}
            return scores.get(authority.lower(), 0.5)

        def score_item(item: dict) -> float:
            base_score = item.get("retrieval_score", 0.5)
            auth_score = get_authority_score(item.get("authority", "medium"))
            return base_score * 0.7 + auth_score * 0.3

        return sorted(evidence_list, key=score_item, reverse=True)
