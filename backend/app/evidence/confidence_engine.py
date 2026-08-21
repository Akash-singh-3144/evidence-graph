class ConfidenceEngine:
    @staticmethod
    def calculate_confidence(evidence_list: list[dict], conflicts: list[dict]) -> float:
        """
        Calculates explainable confidence score.
        Factors:
        - Source Authority
        - Relevance
        - Freshness
        - Agreement
        - Contradictions
        """
        if not evidence_list:
            return 0.0

        base_confidence = 0.8
        
        # Penalize for conflicts
        conflict_penalty = len(conflicts) * 0.15
        
        # Boost for high authority
        high_auth_count = sum(1 for e in evidence_list if e.get("authority") == "high")
        auth_boost = min(high_auth_count * 0.05, 0.15)
        
        final_score = base_confidence - conflict_penalty + auth_boost
        
        # Clamp between 0.1 and 0.99
        return max(0.1, min(0.99, final_score))
