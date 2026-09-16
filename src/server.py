import os
from typing import Dict

from fastapi import FastAPI
from pydantic import BaseModel

from fhir_client import FHIRClient
from llm import LLMClient
from rag import RAGPipeline

app = FastAPI(title="FHIR RAG Assistant")

fhir_client = FHIRClient()
llm_client = LLMClient()
rag_pipeline = RAGPipeline(fhir_client=fhir_client, llm_client=llm_client)


class QueryRequest(BaseModel):
    patient_id: str
    question: str


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/ask")
def ask(query: QueryRequest) -> Dict[str, str]:
    answer = rag_pipeline.answer_question(query.patient_id, query.question)
    return {"answer": answer}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("server:app", host="0.0.0.0", port=int(os.getenv("APP_PORT", "8000")), reload=True)
