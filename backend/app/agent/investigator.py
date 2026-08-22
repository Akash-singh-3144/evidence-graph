from app.agent.planner import InvestigationPlanner
from app.agent.tool_selector import ToolSelector
from app.llm.gemini_client import GeminiClient
from app.evidence.collector import EvidenceCollector
from app.evidence.normalizer import EvidenceNormalizer
from app.evidence.deduplicator import EvidenceDeduplicator
from app.evidence.ranker import EvidenceRanker
from app.evidence.verifier import EvidenceVerifier
from app.evidence.conflict_detector import ConflictDetector
from app.evidence.graph_builder import GraphBuilder
from app.evidence.confidence_engine import ConfidenceEngine
import logging

logger = logging.getLogger(__name__)

class Investigator:
    """Orchestrates the entire investigation state machine pipeline."""
    def __init__(self):
        self.planner = InvestigationPlanner()
        self.tool_selector = ToolSelector()
        self.llm = GeminiClient()

    async def run(self, query: str):
        # 1. Plan
        plan = await self.planner.create_plan(query)
        # 2. Tools
        tools = await self.tool_selector.select_tools(query, plan)
        
        # Enforce PDF and WEB implicit search for all queries unconditionally 
        if "pdf" not in [t.lower() for t in tools]:
            tools.append("pdf")
        if "web" not in [t.lower() for t in tools]:
            tools.append("web")
            
        # 3. Native Agentic Tool Fetching
        collector = EvidenceCollector()
        
        # Determine if database needs to be queried
        if "database" in [t.lower() for t in tools]:
            import httpx
            # 1. Fetch dynamic schema from user's active database
            try:
                async with httpx.AsyncClient() as client:
                    schema_resp = await client.get("http://mcp-db:8003/schema", timeout=30.0)
                    schema_text = schema_resp.text
            except Exception as e:
                schema_text = f"Error fetching schema (Timeout/Connect): {repr(e)}"

            # 2. Generate SQL via Gemini using EXACT schema
            sql_prompt = f"Given the PostgreSQL schema ({schema_text}), generate a SINGLE valid read-only SELECT SQL query to answer this user query: '{query}'. Provide ONLY the raw SQL string without formatting or explanation. If the table uses uppercase letters (like 'Customer'), YOU MUST wrap it in double quotes in the SQL query (e.g. SELECT * FROM public.\"Customer\")."
            sql_query = await self.llm.generate_response(sql_prompt)
            
            import re
            sql_match = re.search(r'```(?:sql)?\n?(.*?)\n?```', sql_query, re.IGNORECASE | re.DOTALL)
            if sql_match:
                sql_query = sql_match.group(1).strip()
            else:
                sql_query = sql_query.replace('```sql', '').replace('```', '').strip()
            
            # 3. Execute dynamically against DB MCP
            try:
                import json
                async with httpx.AsyncClient() as client:
                    resp = await client.post("http://mcp-db:8003/execute", json={"sql": sql_query}, timeout=30.0)
                    try:
                        db_result = json.loads(resp.text)
                    except:
                        db_result = resp.text
                    collector.collect("mcp_postgres", "database", {"result": db_result}, {"query": sql_query, "claim": "Database analytical response fetched natively"})
            except Exception as e:
                pass # Silently drop DB errors so the LLM doesn't falsely blame authentication failures for missing PDF facts

        if any(t.lower() in ["pdf", "web"] for t in tools):
            from app.rag.embeddings.service import EmbeddingService
            from app.rag.vectorstore.qdrant_client import VectorStoreClient
            
            embedder = EmbeddingService()
            q_client = VectorStoreClient()
            try:
                vectors = await embedder.generate_embeddings_batch([query])
                query_vector = vectors[0]
                
                if "pdf" in [t.lower() for t in tools]:
                    pdf_results = await q_client.search(query_vector, source_type="pdf", limit=15)
                    for res in pdf_results:
                        collector.collect("mcp_pdf", "pdf", {"text": res.payload["text"]}, res.payload)
                
                if "web" in [t.lower() for t in tools]:
                    web_results = await q_client.search(query_vector, source_type="web", limit=15)
                    for res in web_results:
                        collector.collect("mcp_web", "web", {"text": res.payload["text"]}, res.payload)
            except Exception as e:
                import traceback
                error_msg = f"Vector Extraction Crash: {repr(e)}\n{traceback.format_exc()}"
                collector.collect("mcp_pdf", "pdf", {"text": error_msg}, {"claim": "CRITICAL VECTOR DB FAILURE", "source_name": "Backend RAG Engine"})
        
        # 4. Engine Process
        raw_evidence = collector.get_all()
        normalized = [EvidenceNormalizer.normalize(e) for e in raw_evidence]
        deduped = EvidenceDeduplicator.deduplicate(normalized)
        ranked = EvidenceRanker.rank(deduped)
        
        relationships = EvidenceVerifier.verify(ranked)
        conflicts = ConflictDetector.detect_conflicts(ranked)
        graph = GraphBuilder.build_graph(query, ranked, relationships, conflicts)
        confidence = ConfidenceEngine.calculate_confidence(ranked, conflicts)
        
        # 5. Synthesis
        synthesis_prompt = (
            f"Synthesize the answer for '{query}' using ONLY the provided evidence array: {ranked}. "
            f"CRITICAL ASSISTANT RULE 1: You are strictly forbidden from using external knowledge. If the answer is not clearly present in the provided evidence array, you MUST respond exactly with: 'The provided documents do not contain the answer to this question.'\n"
            f"CRITICAL ASSISTANT RULE 2: The final conclusion MUST be exactly 2 or 3 lines of text. Do NOT output giant paragraphs, bullet points, code blocks, or SQL logic. Give a dense, exact, short 2-3 line answer.\n"
            f"CRITICAL ASSISTANT RULE 3: If comparing numbers (like ages, votes, metrics) or if a chart/graph is relevant, DO NOT DRAW ASCII CHARTS (e.g. ▇▇). Instead, output a JSON array of the extracted data wrapped exactly in a <chart_data> tag anywhere in your text. Example: <chart_data>[{{\"Name\": \"Huang\", \"Age\": 63}}, {{\"Name\": \"Kress\", \"Age\": 58}}]</chart_data>. The frontend will natively draw it. State confidence {confidence}"
        )
        answer = await self.llm.generate_response(synthesis_prompt)
        
        return {
            "query": query,
            "plan": plan,
            "tools": tools,
            "evidence": ranked,
            "graph": graph,
            "confidence": confidence,
            "answer": answer
        }
