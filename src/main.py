import os
import json
from dotenv import load_dotenv
from anthropic import Anthropic
from src.config import ResearchReport

# Load credentials
load_dotenv()

def run_research_agent(topic: str) -> ResearchReport:
    client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # We pass the Pydantic schema as a tool definition to force a structured JSON output
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1000,
        temperature=0.2, # Low temperature for analytical accuracy
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
        tool_choice={"type": "tool", "name": "generate_report"} # Force Claude to use this tool
    )
    
    # Extract the tool input parsed by Claude
    tool_use = response.content[0]
    structured_data = tool_use.input
    
    return ResearchReport(**structured_data)

if __name__ == "__main__":
    test_topic = "The current state of quantum computing scaling in 2026"
    print(f"🚀 Initializing research agent for topic: '{test_topic}'...\n")
    
    try:
        report = run_research_agent(test_topic)
        print("✅ Report successfully generated with structured formatting:\n")
        print(json.dumps(report.model_dump(), indent=2))
    except Exception as e:
        print(f"❌ Error during agent execution: {e}")
