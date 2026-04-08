from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from tavily import TavilyClient
from app.services.rag import search_chroma
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o",
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Tool 1 — Search through uploaded files using RAG
# The docstring is critical — the Agent reads it to decide whether to use this tool
@tool
def search_uploaded_files(query: str) -> str:
    """
    Search through the user's uploaded files to answer questions.
    Use this tool when the user asks about content from their uploaded documents.
    """
    results = search_chroma(query)
    if not results:
        return "No relevant content found in uploaded files."
    return "\n\n".join([doc.page_content for doc in results])

# Tool 2 — Search the web using Tavily API
@tool
def search_web(query: str) -> str:
    """
    Search the web for current information.
    Use this tool when the question requires up-to-date information
    or when the answer is not found in uploaded files.
    """
    results = tavily.search(query=query, max_results=3)
    return "\n\n".join([r["content"] for r in results["results"]])

# Tool 3 — Summarise long content into a concise response
@tool
def summarise(content: str) -> str:
    """
    Summarise a long piece of content into a concise response.
    Use this tool when the retrieved content is too long or needs to be condensed.
    """
    response = llm.invoke([HumanMessage(
        content=f"Please summarise the following content concisely:\n\n{content}"
    )])
    return response.content

# Register all tools and create the ReAct Agent
# create_react_agent handles the full Thought → Action → Observation loop automatically
tools = [search_uploaded_files, search_web, summarise]
agent = create_react_agent(llm, tools)

def ask_agent(question: str) -> str:
    """
    Main entry point — passes the question to the Agent.
    The Agent decides which tools to use and may call multiple tools
    before returning a final answer.
    """
    result = agent.invoke({
        "messages": [HumanMessage(content=question)]
    })
    # Return the last message, which is the Agent's final answer
    return result["messages"][-1].content