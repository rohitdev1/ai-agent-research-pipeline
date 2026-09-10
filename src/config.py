from pydantic import BaseModel, Field
from typing import List

class ResearchReport(BaseModel):
    title: str = Field(description="The clear, objective headline of the research topic")
    summary: str = Field(description="A concise 3-sentence executive summary of findings")
    key_takeaways: List[str] = Field(description="Bullet points outlining the core facts uncovered")
    confidence_score: float = Field(description="Self-evaluated precision metric between 0.0 and 1.0 based on data availability")
