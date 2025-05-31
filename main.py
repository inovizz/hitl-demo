from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from dotenv import load_dotenv

from models import (
    WorkflowStartRequest, 
    FeedbackRequest, 
    CampaignResponse, 
    StatusResponse, 
    FeedbackResponse,
    AgentState
)
from services import OpenAIService, SessionManager
from workflow import CampaignWorkflowNodes # Ensure this is imported as you are directly using its nodes


load_dotenv()


app = FastAPI(
    title="Marketing Campaign HITL Workflow",
    description="AI-driven marketing campaign strategy with human oversight for brand safety and ethics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

session_manager = SessionManager()
active_workflows = {}


@app.get("/")
async def root():
    return {
        "message": "Marketing Campaign HITL Workflow API",
        "documentation": "/docs",
        "health_check": "/health",
        "example_workflows": {
            "aggressive_approval": "Start workflow → approve (demonstrates poor outcome)",
            "brand_safety_check": "Start → request_info: brand safety concerns → revise → approve",
            "cultural_sensitivity": "Start → request_info: cultural implications → revise → approve",
            "competitor_analysis": "Start → request_info: competitor strategies → revise → approve",
            "escalation": "Start → escalate: requires CMO approval"
        }
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "active_sessions": len(session_manager.sessions),
        "service": "Marketing Campaign HITL Workflow"
    }


@app.post("/start_campaign_workflow", response_model=CampaignResponse)
async def start_campaign_workflow(request: WorkflowStartRequest):
    try:
        if not os.getenv("OPENAI_API_KEY"):
            raise HTTPException(
                status_code=400, 
                detail="OPENAI_API_KEY environment variable is not set. Please add it to your .env file."
            )
        
        print(f"🔧 Initializing OpenAI service...")
        openai_service = OpenAIService()
        print(f"✅ OpenAI service initialized successfully")
        
        workflow_nodes = CampaignWorkflowNodes(openai_service) # Use CampaignWorkflowNodes
        
        initial_state: AgentState = {
            "current_proposal": "",
            "initial_proposal": "", # Ensure initial_proposal is part of AgentState
            "human_feedback": "",
            "status": "initializing",
            "iteration": 0,
            "feedback_history": [],
            "info_requested_query": "",
            "context_info": "",
            "campaign_objective": f"Launch campaign for {request.product_name}: {request.campaign_goal}",
            "target_audience": "Health-conscious millennials aged 25-40",
            "budget_allocation": request.total_budget,
            "brand_guidelines": "Maintain brand authenticity and social responsibility"
        }
        
        session_id = session_manager.create_session(initial_state)
        active_workflows[session_id] = workflow_nodes # Store the nodes instance
        
        print(f"\n🚀 Starting marketing campaign workflow: {session_id}")
        print(f"📱 Product: {request.product_name}")
        print(f"🎯 Goal: {request.campaign_goal}")
        print(f"💰 Budget: {request.total_budget}")
        
        processed_state = workflow_nodes.initial_analysis_node(initial_state)
        session_manager.update_session(session_id, processed_state)
        
        return CampaignResponse(
            session_id=session_id,
            # REMOVED STRING SLICING HERE
            current_proposal=processed_state["current_proposal"], 
            status=processed_state["status"],
            iteration=processed_state["iteration"],
            message="Campaign workflow started. AI has generated initial aggressive marketing strategy.",
            campaign_details={
                "product": request.product_name,
                "goal": request.campaign_goal,
                "budget": request.total_budget
            }
        )
    
    except ValueError as ve:
        print(f"🚨 Configuration Error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(f"🚨 Unexpected Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to start campaign workflow: {str(e)}")


@app.get("/campaign_status/{session_id}", response_model=StatusResponse)
async def get_campaign_status(session_id: str):
    if not session_manager.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Campaign session not found")
    
    state = session_manager.get_session(session_id)
    
    return StatusResponse(
        session_id=session_id,
        current_proposal=state["current_proposal"],
        status=state["status"],
        iteration=state["iteration"],
        feedback_history=state["feedback_history"],
        # REMOVED STRING SLICING HERE
        context_info=state.get("context_info", ""), 
        initial_proposal=state.get("initial_proposal", ""), # Ensure this is passed correctly
        campaign_details={
            "objective": state["campaign_objective"],
            "budget": state["budget_allocation"],
            "target_audience": state["target_audience"]
        }
    )


@app.post("/submit_campaign_feedback/{session_id}", response_model=FeedbackResponse)
async def submit_campaign_feedback(session_id: str, feedback_request: FeedbackRequest):
    if not session_manager.session_exists(session_id):
        raise HTTPException(status_code=404, detail="Campaign session not found")
    
    if session_manager.is_terminal_state(session_id):
        state = session_manager.get_session(session_id)
        raise HTTPException(
            status_code=400, 
            detail=f"Campaign workflow already completed with status: {state['status']}"
        )
    
    if session_id not in active_workflows:
        raise HTTPException(status_code=400, detail="Workflow not found for this session")
    
    try:
        print(f"\n📨 Campaign feedback received for session {session_id}: {feedback_request.feedback}")
        
        current_state = session_manager.get_session(session_id)
        current_state["human_feedback"] = feedback_request.feedback
        
        workflow_nodes = active_workflows[session_id] # Retrieve the nodes instance
        
        final_state = workflow_nodes.feedback_revision_node(current_state) # Direct call
        
        session_manager.update_session(session_id, final_state)
        
        return FeedbackResponse(
            message="Campaign feedback processed successfully",
            new_state={
                # REMOVED STRING SLICING HERE
                "current_proposal": final_state["current_proposal"],
                "status": final_state["status"],
                "iteration": final_state["iteration"],
                "feedback_history": final_state["feedback_history"]
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing campaign feedback: {str(e)}")


@app.get("/sessions")
async def list_sessions():
    return {
        "total_sessions": len(session_manager.sessions),
        "sessions": [
            {
                "session_id": sid,
                "status": state["status"],
                "iteration": state["iteration"],
                "campaign": state["campaign_objective"][:50] + "..."
            }
            for sid, state in session_manager.sessions.items()
        ]
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
