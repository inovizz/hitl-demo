import uuid
import os
from typing import Dict
from openai import OpenAI
from models import AgentState
from dotenv import load_dotenv

load_dotenv()


class OpenAIService:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        try:
            self.client = OpenAI(api_key=api_key, timeout=30.0, max_retries=2)
            self._test_client()
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI client: {str(e)}")

    def _test_client(self):
        """Test the OpenAI client to ensure it's working properly"""
        try:
            self.client.models.list()
        except Exception as e:
            raise ValueError(f"OpenAI client test failed: {str(e)}")

    def get_completion(
        self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
    ) -> str:
        try:
            response = self.client.chat.completions.create(
                # Ensure the model here is capable of longer outputs if needed, 'gpt-4o-mini' is generally good
                model="gpt-4o-mini", # Used to be gpt-4 in provided code
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            return response.choices[0].message.content
        except Exception as e:
            error_msg = f"OpenAI API Error: {str(e)}"
            print(f"🚨 {error_msg}")
            return f"Error generating AI response: {str(e)}"


class SessionManager:
    def __init__(self):
        self.sessions: Dict[str, AgentState] = {}

    def create_session(self, state: AgentState) -> str:
        session_id = str(uuid.uuid4())
        self.sessions[session_id] = state
        return session_id

    def get_session(self, session_id: str) -> AgentState:
        return self.sessions.get(session_id)

    def update_session(self, session_id: str, state: AgentState):
        self.sessions[session_id] = state

    def session_exists(self, session_id: str) -> bool:
        return session_id in self.sessions

    def is_terminal_state(self, session_id: str) -> bool:
        if not self.session_exists(session_id):
            return False
        status = self.sessions[session_id]["status"]
        return status == "completed"


class PromptService:
    @staticmethod
    def get_initial_analysis_prompt(state: AgentState) -> str:
        return f"""
        You are an AI marketing strategist tasked with creating an aggressive campaign strategy. Focus primarily on maximizing conversions and market penetration.

        Campaign Details:
        - Product: {state.get('campaign_objective', 'New product launch')}
        - Budget: {state.get('budget_allocation', '$500,000')}
        - Target: {state.get('target_audience', 'Health-conscious millennials')}

        Create a marketing campaign proposal that maximizes ROI and conversion rates. Be aggressive with targeting and messaging. Focus on:
        1. Campaign strategy and messaging
        2. Channel allocation and budget distribution
        3. Target audience segmentation
        4. Timeline and KPIs
        5. Creative direction

        Format as a business proposal with specific budget allocations and tactics.
        Be aggressive and conversion-focused - don't worry about brand safety or cultural sensitivity at this stage.
        """

    @staticmethod
    def get_revision_prompt(state: AgentState) -> str:
        return f"""
        You are revising a marketing campaign based on human feedback. 

        Original Proposal:
        {state['current_proposal']}

        Human Feedback:
        {state['human_feedback']}

        Additional Context (if any):
        {state['context_info']}

        Previous Feedback History:
        {'; '.join(state['feedback_history'])}

        Create a revised campaign proposal that specifically addresses the human feedback while maintaining campaign effectiveness. Consider:
        - Brand safety and reputation
        - Cultural sensitivity
        - Regulatory compliance
        - Long-term brand value vs short-term gains
        - Stakeholder concerns
        - Ethical marketing practices

        Provide a complete revised proposal with explanations of changes made.
        """
    
    @staticmethod
    def get_information_gathering_prompt(state: AgentState) -> str:
        return f"""
        You are a marketing research analyst gathering specific information for a campaign strategy.

        Current Campaign Proposal:
        {state['current_proposal']}

        Information Request:
        {state['info_requested_query']}

        Provide detailed research and analysis on the requested topic. Include:
        - Relevant data and statistics
        - Industry best practices
        - Potential risks and concerns
        - Regulatory considerations
        - Competitor analysis (if relevant)
        - Cultural and social considerations

        Be thorough and provide actionable insights that will help improve the campaign strategy.
        """
    
    # The get_proposal_update_prompt was commented out in your latest provided services.py,
    # so keeping it commented out.
    # @staticmethod
    # def get_proposal_update_prompt(gathered_info: str, current_proposal: str) -> str:
    #     return f"""
    #     Based on this research: {gathered_info}
        
    #     Update the current campaign proposal: {current_proposal}
        
    #     Incorporate the findings and provide an updated strategy that addresses any concerns or opportunities identified in the research.
    #     Keep the same format but integrate the new insights meaningfully.
    #     """