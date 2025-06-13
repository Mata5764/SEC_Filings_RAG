from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.rag.chain import query_rag

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

@app.post("/query", response_model=QueryResponse)
def query_endpoint(request: QueryRequest):
    try:
        # Call query_rag with the question from the request
        answer = query_rag(request.question)
        return QueryResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 