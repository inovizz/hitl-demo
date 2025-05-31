from langgraph.graph import StateGraph, END
from models import AgentState
from services import OpenAIService, PromptService


class CampaignWorkflowNodes:
    def __init__(self, openai_service: OpenAIService):
        self.openai_service = openai_service
        self.prompt_service = PromptService()

    def initial_analysis_node(self, state: AgentState) -> AgentState:
        print("🤖 AI: Generating initial strategy without human input...")

        prompt = self.prompt_service.get_initial_analysis_prompt(state)
        # INCREASE MAX_TOKENS SIGNIFICANTLY HERE
        ai_proposal = self.openai_service.get_completion(prompt, max_tokens=1500) # Increased from 300

        return {
            **state,
            "current_proposal": ai_proposal,
            "initial_proposal": ai_proposal,
            "status": "awaiting_feedback",
            "iteration": 1,
            "feedback_history": [],
            "context_info": "",
            "human_feedback": "",
        }

    def feedback_revision_node(self, state: AgentState) -> AgentState:
        print("🔄 AI: Revising strategy based on human feedback...")
        
        # Use the PromptService's get_revision_prompt for consistency and easier modification
        prompt = self.prompt_service.get_revision_prompt(state) # Changed from hardcoded string
        
        # INCREASE MAX_TOKENS SIGNIFICANTLY HERE
        revised_proposal = self.openai_service.get_completion(prompt, max_tokens=1500) # Increased from 400
        
        feedback_history = state.get("feedback_history", [])
        feedback_history.append(state["human_feedback"])

        return {
            **state,
            "current_proposal": revised_proposal,
            "status": "completed",
            "iteration": state["iteration"] + 1,
            "feedback_history": feedback_history,
            "human_feedback": "",
        }

def decide_next_node(state: AgentState) -> str:
    if state["status"] == "awaiting_feedback" and state["human_feedback"]:
        return "feedback_revision"
    elif state["status"] == "completed":
        return END
    else:
        return "initial_analysis"


class CampaignWorkflow:
    def __init__(self, openai_service: OpenAIService):
        self.nodes = CampaignWorkflowNodes(openai_service)
        self.graph = self._create_graph()

    def _create_graph(self):
        workflow = StateGraph(AgentState)

        workflow.add_node("initial_analysis", self.nodes.initial_analysis_node)
        workflow.add_node("feedback_revision", self.nodes.feedback_revision_node)
        workflow.set_entry_point("initial_analysis")
        workflow.add_edge("initial_analysis", END)
        return workflow.compile()
