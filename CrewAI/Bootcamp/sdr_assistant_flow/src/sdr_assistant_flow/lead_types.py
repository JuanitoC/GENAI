from pydantic import BaseModel, Field
from typing import Optional, List

class LeadPersonalInfo(BaseModel):
    name: str = Field(..., description="The full name of the lead.")
    job_title: str = Field(..., description="The job title of the lead.")
    role_relevance: int = Field(..., ge=0, le=10, description="Score indicating the lead’s influence in the buying process (0–10).")
    professional_background: Optional[str] = Field(None, description="Brief highlights of the lead’s professional background or career.")

class CompanyInfo(BaseModel):
    company_name: str = Field(..., description="Name of the company the lead works for.")
    industry: str = Field(..., description="The sector or industry of the company.")
    company_size: int = Field(..., description="Estimated number of employees at the company.")
    revenue: Optional[float] = Field(None, description="Annual revenue of the company, if publicly available.")
    market_presence: int = Field(..., ge=0, le=10, description="Visibility or influence the company has in its market (0–10).")

class EngagementFit(BaseModel):
    readiness_score: int = Field(..., ge=0, le=10, description="Assessment of how ready and relevant the lead is for outreach (0–10).")
    alignment_notes: Optional[str] = Field(None, description="Supporting notes that explain the rationale for the readiness score.")

class LeadReadinessScore(BaseModel):
    score: int = Field(..., ge=0, le=100, description="Final lead readiness score (0–100).")
    scoring_criteria: List[str] = Field(..., description="List of criteria that contributed to the final score.")
    summary_notes: Optional[str] = Field(None, description="Any validation comments or strategic notes about the score.")

class LeadReadinessResult(BaseModel):
    personal_info: LeadPersonalInfo = Field(..., description="Detailed profile of the lead.")
    company_info: CompanyInfo = Field(..., description="Business context and company insights.")
    engagement_fit: EngagementFit = Field(..., description="Evaluation of how appropriate the timing and message would be for outreach.")
    readiness_score: LeadReadinessScore = Field(..., description="Overall scoring of the lead’s outreach potential.")
