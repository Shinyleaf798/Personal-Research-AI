from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Personal AI Research Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React 前端
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "AI Research Agent is running!"}