from fastapi import FastAPI
from app.routers import agent, upload
from app.database import engine
from app.models import history
from app.database import Base

# Create all tables on startup if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(agent.router)
app.include_router(upload.router)

@app.get("/")
def root():
    return {"status": "AI Research Agent is running"}