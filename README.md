# Personal AI Research Agent

Personal AI Research Agent is a full-stack AI research assistant that can automatically perform web search, document retrieval, information synthesis, and report generation based on a user's question, with source citations included.

## 🤖 Features

1. 🤔 Smart Q&A  
The system analyzes the user's query and generates structured answers or research-style reports.

2. 🌐📄 Combined Web and Document Retrieval  
It supports both web search and local document reading, allowing the system to combine real-time information with private knowledge sources.

3. 📚 RAG Knowledge Base  
Users can upload PDF and TXT files, which are processed into a vector-based knowledge base for semantic retrieval and more accurate answers.

4. 📝 Source Citations  
Each response includes references to its information sources, such as websites and document sections, improving transparency and trustworthiness.

5. 🕘 History Tracking  
All questions and generated reports are stored in the database for future review and reuse.

## ⚙️ Tech Stack

- ⚛️ Frontend: React  
Handles user input, result display, and history browsing.

- ⚡ Backend: FastAPI  
Manages APIs, agent orchestration, model calls, and data handling.

- 🧠 AI Workflow: LangGraph + ReAct Agent  
Controls the workflow, reasoning process, and tool selection.

- 🔎 Retrieval Layer: Tavily API + RAG + ChromaDB  
Supports both real-time web search and semantic document retrieval.

- 🗄️ Database: PostgreSQL  
Stores query history and generated reports.

## ✨ Highlights

This project is more than a simple Q&A system. It is an AI research assistant that automates the full pipeline of retrieval, synthesis, report generation, and source citation. It also has a complete full-stack architecture and can be extended into a multi-agent system in future versions.