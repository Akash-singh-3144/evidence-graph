from app.llm.gemini_client import GeminiClient

class InvestigationPlanner:
    def __init__(self):
        self.llm = GeminiClient()

    async def create_plan(self, query: str) -> list[str]:
        prompt = f"""
        You are an Investigation Planner for EvidenceGraph.
        User Query: {query}
        Create a 3 to 6 step investigation plan. Output JSON:
        {{ "plan": ["step 1", "step 2"] }}
        """
        response = await self.llm.generate_response(prompt, schema=True)
        return response.get("plan", [])
