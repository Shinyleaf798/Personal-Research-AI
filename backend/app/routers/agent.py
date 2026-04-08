from fastapi import APIRouter
from pydantic import BaseModel
from app.services.agent import ask_agent

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/agent")
def agent(request: QuestionRequest):
    """
    Unified entry point — no need to manually select tools
    The Agent will decide for itself:
    - If the question is about uploaded files → use search_uploaded_files
    - If the question requires the latest information → use search_web
    - If the content is too long and needs to be condensed → use summarise
    """
    answer = ask_agent(request.question)
    return {"answer": answer}