from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from compiler.pipeline import CompilerPipeline
from schemas import AppSchema
from runtime.simulator import execute_schema

load_dotenv()

app = FastAPI(title="AI Compiler API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerateRequest(BaseModel):
    prompt: str

class ExecuteRequest(BaseModel):
    schema_data: AppSchema

@app.post("/generate", response_model=AppSchema)
async def generate_app(request: GenerateRequest):
    try:
        pipeline = CompilerPipeline(max_retries=2)
        app_schema = pipeline.compile(request.prompt)
        return app_schema
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute")
async def execute_app(request: ExecuteRequest):
    try:
        result = execute_schema(request.schema_data)
        if result["status"] == "error":
            raise HTTPException(status_code=400, detail=result["message"])
        return result
    except Exception as e:
         raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}
