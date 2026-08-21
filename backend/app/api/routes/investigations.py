from fastapi import APIRouter
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: str

router = APIRouter()

@router.post("/query")
async def start_investigation(request: QueryRequest):
    from app.agent.investigator import Investigator
    
    investigator = Investigator()
    result = await investigator.run(request.query)
    
    return {
        "status": "success",
        "investigation_id": "simulated_id",
        "result": result
    }

@router.get("/{id}")
async def get_investigation(id: str):
    return {"status": "ok", "id": id, "data": "simulated_investigation"}
