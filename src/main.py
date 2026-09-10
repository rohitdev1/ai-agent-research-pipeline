import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from src.config import ResearchReport

# Load environment variables
load_dotenv()

app = FastAPI(title="AI Agent Research Pipeline API")

def run_research_agent(topic: str) -> ResearchReport:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        raise ValueError("Missing ANTHROPIC_API_KEY environment variable.")

    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0.2,
        system="You are an expert AI Research Assistant. Gather data, analyze objectively, and compile structured insights.",
        messages=[
            {"role": "user", "content": f"Conduct an in-depth research breakdown on the following topic: {topic}"}
        ],
        tools=[
            {
                "name": "generate_report",
                "description": "Format the final research findings into the structured schema.",
                "input_schema": ResearchReport.model_json_schema()
            }
        ],
        tool_choice={"type": "tool", "name": "generate_report"}
    )
    
    # Extract the tool input parsed by Claude safely
    tool_use = response.content[0]
    structured_data = tool_use.input
    
    return ResearchReport(**structured_data)

# Request schema for the API endpoint
class ResearchRequest(BaseModel):
    topic: str

@app.post("/api/research", response_model=ResearchReport)
async def get_research(request: ResearchRequest):
    try:
        report = run_research_agent(request.topic)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI Server on http://127.0.0.1:8000")
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
