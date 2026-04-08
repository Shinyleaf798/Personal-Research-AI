from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class QueryHistory(Base):
    """
    Stores every question and answer from the Agent.
    Each row represents one conversation turn.
    """
    __tablename__ = "query_history"

    # Primary key — auto increments for each new record
    id = Column(Integer, primary_key=True, index=True)

    # The question the user asked
    question = Column(Text, nullable=False)

    # The Agent's answer
    answer = Column(Text, nullable=False)

    # Which tool the Agent used — "rag", "web_search", or "both"
    tool_used = Column(String(50), nullable=True)

    # Hash of the uploaded file if RAG was used
    file_hash = Column(String(64), nullable=True)

    # Timestamp — automatically set to current time when record is created
    created_at = Column(DateTime(timezone=True), server_default=func.now())