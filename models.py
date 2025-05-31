from typing import Dict, List, TypedDict, Optional, Any
from pydantic import BaseModel, Field
from enum import Enum


class WorkflowStatus(str, Enum):
    INITIALIZING = "initializing"
    AWAITING_FEEDBACK = "awaiting_feedback"
    COMPLETED = "completed"


class AgentState(TypedDict):
    current_proposal: str
    initial_proposal: str
    human_feedback: str
    status: str
    iteration: int
    feedback_history: List[str]
    info_requested_query: str
    context_info: str
    campaign_objective: str
    target_audience: str
    budget_allocation: str
    brand_guidelines: str


class WorkflowStartRequest(BaseModel):
    product_name: str = Field(
        default="EcoFresh Organic Smoothies", description="Product or service name"
    )
    campaign_goal: str = Field(
        default="Launch new organic smoothie line targeting health-conscious millennials",
        description="Campaign objective and goals",
    )
    total_budget: str = Field(default="$500,000", description="Total campaign budget")


class FeedbackRequest(BaseModel):
    feedback: str = Field(..., description="Human feedback for the campaign proposal")


class CampaignResponse(BaseModel):
    session_id: str
    current_proposal: str
    status: str
    iteration: int
    message: str
    campaign_details: Optional[Dict[str, str]] = None


class StatusResponse(BaseModel):
    session_id: str
    current_proposal: str
    status: str
    iteration: int
    feedback_history: List[str]
    context_info: str
    initial_proposal: str = Field(
        ..., description="The initial AI-generated proposal before any human feedback."
    )
    campaign_details: Dict[str, str]


class FeedbackResponse(BaseModel):
    message: str
    new_state: Dict[str, Any]
