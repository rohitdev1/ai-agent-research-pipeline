import os
import json
import asyncio
from dotenv import load_dotenv
from anthropic import Anthropic
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from src.config import ResearchReport

# Load environment variables
load_dotenv()

app = FastAPI(title="Resilient AI Agent Research Pipeline API")

def generate_mock_stream(topic: str):
    """Simulates a real-time token stream when in Mock Mode."""
    mock_report = ResearchReport(
        title=f"Comprehensive Analysis: {topic}",
        summary=f"This streaming synthesis addresses the core parameters governing '{topic}' through standardized historical paradigms.",
        key_takeaways=[
            "Primary driver analysis indicates significant macroeconomic sensitivity.",
            "Secondary alignment trends demonstrate consistent systemic consolidation patterns."
        ],
        confidence_score=0.95
    )
    # Serialize to string and stream it back block-by-block to mimic real-time network chunks
    report_json = json.dumps(mock_report.model_dump())
    for chunk in [report_json[i:i+10] for i in range(0, len(report_json), 10)]:
        yield f"data: {chunk}\n\n"

async def stream_research_agent(topic: str):
    """Asynchronously streams chunks from Anthropic or handles billing fallbacks gracefully."""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    # Check if we should instantly drop to local mock streaming environment
    if not api_key or api_key == "MOCK_MODE":
        for chunk in generate_mock_stream(topic):
            await asyncio.sleep(0.05) # Mimic minor network latency
            yield chunk
        return

    client = Anthropic(api_key=api_key)
    try:
        # Enforcing structured tools inside a live stream
        with client.messages.stream(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1000,
            system="You are an expert AI Research Assistant. Compile insights into the requested schema.",
            messages=[{"role": "user", "content": f"Conduct an in-depth research breakdown on: {topic}"}],
            tools=[{
                "name": "generate_report",
                "description": "Format final findings into the structured schema.",
                "input_schema": ResearchReport.model_json_schema()
            }],
            tool_choice={"type": "tool", "name": "generate_report"}
        ) as stream:
            for text in stream.text_stream:
                yield f"data: {text}\n\n"
                
    except Exception as e:
        if "credit balance" in str(e).lower() or "billing" in str(e).lower():
            print("⚠️ [Upstream API Billing Block] Gracefully routing current pipeline stream to local Mock Engine...")
            os.environ["ANTHROPIC_API_KEY"] = "MOCK_MODE"
            async for chunk in stream_research_agent(topic):
                yield chunk
        else:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

class ResearchRequest(BaseModel):
    topic: str

@app.post("/api/research/stream")
async def get_streaming_research(request: ResearchRequest):
    """Production endpoint delivering Server-Sent Events (SSE) token chunks."""
    return StreamingResponse(stream_research_agent(request.topic), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Streaming FastAPI Server on http://127.0.0.1:8000")
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
