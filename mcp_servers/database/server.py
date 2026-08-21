from fastapi import FastAPI
import asyncpg
import os
import json
from pydantic import BaseModel

app = FastAPI(title="Database Exec Server")

DB_URL = os.getenv("TARGET_DATABASE_URL", "postgresql://user:password@postgres-target:5432/target_db")

@app.get("/schema")
async def get_schema() -> str:
    try:
        conn = await asyncpg.connect(DB_URL)
        tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        await conn.close()
        return "Available Tables: " + ", ".join([t['table_name'] for t in tables])
    except Exception as e:
        return f"Error fetching schema: {str(e)}"

async def get_tables() -> list[str]:
    conn = await asyncpg.connect(DB_URL)
    tables = await conn.fetch("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    await conn.close()
    return [t['table_name'] for t in tables]

async def get_table_schema(table: str) -> str:
    conn = await asyncpg.connect(DB_URL)
    cols = await conn.fetch("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = $1", table)
    await conn.close()
    return f"Schema for {table}: " + ", ".join([f"{c['column_name']} ({c['data_type']})" for c in cols])

async def execute_readonly_query(sql: str) -> str:
    # Validator for SELECT-only
    sql_upper = sql.upper()
    if any(forbidden in sql_upper for forbidden in ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]):
        return "ERROR: Only read-only SELECT queries are allowed."
    
    try:
        conn = await asyncpg.connect(DB_URL)
        try:
            async with conn.transaction(readonly=True):
                rows = await conn.fetch(sql)
                results = [dict(record) for record in rows]
                for row in results:
                    for k, v in row.items():
                        row[k] = str(v)
                return json.dumps(results)
        finally:
            await conn.close()
    except Exception as e:
        return f"Database Error: {str(e)}"

class SqlRequest(BaseModel):
    sql: str

class ConfigRequest(BaseModel):
    db_url: str

@app.post("/config")
async def update_config(req: ConfigRequest):
    global DB_URL
    try:
        conn = await asyncpg.connect(req.db_url, timeout=5)
        await conn.close()
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Database Connection Failed: {str(e)}")
        
    DB_URL = req.db_url
    return {"status": "success", "db_url": "updated"}

@app.post("/execute")
async def direct_execute(req: SqlRequest):
    return await execute_readonly_query(req.sql)
