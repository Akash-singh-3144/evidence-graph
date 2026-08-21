from app.llm.gemini_client import GeminiClient

class ToolSelector:
    def __init__(self):
        self.llm = GeminiClient()

    async def select_tools(self, query: str, plan: list[str]) -> list[str]:
        prompt = f"""
        Determine the most appropriate RAG tools to solve this investigation.
        Query: {query}
        Execution Plan: {plan}
        
        CRITICAL RULES for Tool Selection:
        1. "pdf" -> STRICTLY HIGHEST PRIORITY. You MUST select 'pdf' for almost all questions, especially if they are about concepts, internal knowledge, business logic, or general inquiries, because the User uploaded custom documents into the Qdrant PDF vector store!
        2. "database" -> Select ONLY if the user explicitly asks for quantitative tabular data, numbers, charts, or company SQL metrics.
        3. "web" -> STRICTLY LOWEST PRIORITY. Select ONLY if the user explicitly demands real-time internet search, live news, or external public links.

        Available tools array: ["pdf", "web", "database"]
        Return ONLY valid JSON wrapping the array: {{ "tools": ["..."] }}
        """
        response = await self.llm.generate_response(prompt, schema=True)
        return response.get("tools", [])
