class GraphBuilder:
    @staticmethod
    def build_graph(query: str, evidence_list: list[dict], relationships: list[dict], conflicts: list[dict]) -> dict:
        """
        Constructs a React Flow compatible JSON structure.
        """
        nodes = []
        edges = []

        # Root Node
        nodes.append({
            "id": "root_query",
            "type": "QUERY",
            "data": {"label": query},
            "position": {"x": 250, "y": 0}
        })

        y_offset = 100
        x_offset = 0

        for i, ev in enumerate(evidence_list):
            node_id = f"ev_{ev['evidence_id']}"
            nodes.append({
                "id": node_id,
                "type": "EVIDENCE",
                "data": {"label": ev["claim"] or ev["source_name"], "detail": ev},
                "position": {"x": x_offset, "y": y_offset}
            })
            edges.append({
                "id": f"edge_root_{node_id}",
                "source": "root_query",
                "target": node_id,
                "label": "SUPPORTED_BY"
            })
            x_offset += 200

        # Map conflicts
        for conflict in conflicts:
            edges.append({
                "id": f"conflict_{conflict['evidence_a']}_{conflict['evidence_b']}",
                "source": f"ev_{conflict['evidence_a']}",
                "target": f"ev_{conflict['evidence_b']}",
                "label": "CONTRADICTS",
                "animated": True,
                "style": {"stroke": "red"}
            })

        return {"nodes": nodes, "edges": edges}
