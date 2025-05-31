import streamlit as st
import requests
import json
import time
from typing import Dict, Any, Optional


class MarketingCampaignUI:
    def __init__(self, api_base_url: str = "http://127.0.0.1:8000"):
        self.api_base_url = api_base_url

    def start_campaign(
        self, product: str, goal: str, budget: str
    ) -> Optional[Dict[str, Any]]:
        try:
            response = requests.post(
                f"{self.api_base_url}/start_campaign_workflow",
                json={
                    "product_name": product,
                    "campaign_goal": goal,
                    "total_budget": budget,
                },
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Failed to start campaign: {e}")
            return None

    def submit_feedback(
        self, session_id: str, feedback: str
    ) -> Optional[Dict[str, Any]]:
        try:
            response = requests.post(
                f"{self.api_base_url}/submit_campaign_feedback/{session_id}",
                json={"feedback": feedback},
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Failed to submit feedback: {e}")
            return None

    def get_status(self, session_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get(f"{self.api_base_url}/campaign_status/{session_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Failed to get status: {e}")
            return None

    def check_api_health(self) -> bool:
        try:
            response = requests.get(f"{self.api_base_url}/health")
            return response.status_code == 200
        except:
            return False


def display_status_badge(status: str):
    status_colors = {"initializing": "🔄", "awaiting_feedback": "⏳", "completed": "✅"}

    status_descriptions = {
        "initializing": "Starting campaign analysis",
        "awaiting_feedback": "Awaiting human feedback",
        "completed": "Campaign workflow completed",
    }

    emoji = status_colors.get(status, "❓")
    description = status_descriptions.get(status, status)

    st.write(f"{emoji} **{description}**")


def display_proposal(proposal: str, max_length: int = 1000):
    if len(proposal) > max_length:
        with st.expander("📋 Campaign Proposal (Click to expand)", expanded=False):
            st.write(proposal)
    else:
        st.subheader("📋 Current Campaign Proposal")
        st.write(proposal)


def display_feedback_history(feedback_history: list):
    if feedback_history:
        st.subheader("💭 Feedback History")
        for i, feedback in enumerate(feedback_history, 1):
            st.write(f"**{i}.** {feedback}")


def main():
    st.set_page_config(
        page_title="Marketing Campaign HITL", page_icon="🎯", layout="wide"
    )

    st.title("🎯 Marketing Campaign Generator")
    st.markdown(
        "*Demonstrating the importance of human oversight in AI-driven marketing campaigns*"
    )

    ui = MarketingCampaignUI()

    if not ui.check_api_health():
        st.error(
            "🚨 FastAPI backend is not running. Please start it with: `python main.py`"
        )
        st.stop()

    if "session_id" not in st.session_state:
        st.session_state.session_id = None
    if "campaign_data" not in st.session_state:
        st.session_state.campaign_data = None

    with st.sidebar:
        st.header("Demo Scenarios")

        demo_scenarios = {
            "Digital Lending Platform": {
                "product": "InstantRupee Personal Loans",
                "goal": "Maximize loan approvals for urgent cash needs across Tier-2 and Tier-3 cities",
                "budget": "₹2 Crores",
                "risk": "⚠️ RBI compliance risk: ₹10-50 Crore penalties for predatory lending",
            },
            "Ayurvedic Health Products": {
                "product": "AyurSlim Weight Loss Capsules",
                "goal": "Drive sales with guaranteed weight loss claims using traditional Ayurvedic messaging",
                "budget": "₹3 Crores",
                "risk": "⚠️ AYUSH Ministry violation: ₹5-25 Crore fines for false medical claims",
            },
            "EdTech Coaching Platform": {
                "product": "CrackJEE Guaranteed Success Program",
                "goal": "Promise 100% IIT admission success to attract desperate students and parents",
                "budget": "₹5 Crores",
                "risk": "⚠️ Consumer Protection Act: ₹2-15 Crore penalties for misleading education claims",
            },
            "Investment Advisory App": {
                "product": "StockSure Trading Tips",
                "goal": "Guarantee 300% returns in stock market with insider tips and sure-shot recommendations",
                "budget": "₹4 Crores",
                "risk": "⚠️ SEBI violation: ₹25-100 Crore penalties for unauthorized investment advisory",
            },
        }

        selected_demo = st.selectbox(
            "Select Demo Scenario", ["Custom"] + list(demo_scenarios.keys())
        )

        if selected_demo != "Custom" and selected_demo in demo_scenarios:
            scenario = demo_scenarios[selected_demo]

            st.success(f"**{selected_demo} Demo**")
            st.write(f"**Product**: {scenario['product']}")
            st.write(f"**Goal**: {scenario['goal']}")
            st.write(f"**Budget**: {scenario['budget']}")
            st.error(f"**Risk**: {scenario['risk']}")

            if st.button(f"🚀 Start {selected_demo} Campaign", type="primary"):
                with st.spinner("🤖 AI is generating initial strategy..."):
                    result = ui.start_campaign(
                        scenario["product"], scenario["goal"], scenario["budget"]
                    )
                    if result:
                        st.session_state.session_id = result["session_id"]
                        st.session_state.campaign_data = result
                        st.success("Campaign started successfully!")
                        st.rerun()

        st.markdown("---")

        if selected_demo == "Custom":
            st.header("📊 Custom Campaign Setup")

            product_name = st.text_input(
                "Product/Service Name", value="SwiggyFast Food Delivery"
            )

            campaign_goal = st.text_area(
                "Campaign Goal",
                value="Expand food delivery services to Tier-2 cities across India with aggressive pricing and fast delivery promises",
                height=100,
            )

            budget = st.selectbox(
                "Campaign Budget",
                [
                    "₹50 Lakhs",
                    "₹1 Crore",
                    "₹2 Crores",
                    "₹5 Crores",
                    "₹10 Crores",
                    "₹25 Crores",
                ],
            )

            if st.button("🚀 Start Custom Campaign", type="primary"):
                with st.spinner("🤖 AI is generating initial strategy..."):
                    result = ui.start_campaign(product_name, campaign_goal, budget)
                    if result:
                        st.session_state.session_id = result["session_id"]
                        st.session_state.campaign_data = result
                        st.success("Campaign started successfully!")
                        st.rerun()

    main_content_col = st.columns(1)[0]

    with main_content_col:
        st.header("🚀 Campaign Management")

        if not st.session_state.session_id:
            st.info("👈 **Select a demo scenario from the sidebar to begin**")
        else:
            if st.button("Reset Campaign"):
                st.session_state.session_id = None
                st.session_state.campaign_data = None
                st.rerun()

        if st.session_state.session_id:
            status_data = ui.get_status(st.session_state.session_id)

            if status_data:
                st.subheader(
                    f"📊 Campaign Status - Session: {st.session_state.session_id[:8]}..."
                )

                col1_status, col2_status, col3_status = st.columns(3)
                with col1_status:
                    display_status_badge(status_data["status"])
                with col2_status:
                    st.metric("Iteration", status_data["iteration"])
                with col3_status:
                    st.metric("Budget", status_data["campaign_details"]["budget"])

                display_proposal(status_data["current_proposal"])

                # if status_data["status"] == "awaiting_feedback":
                #     st.warning(
                #         "⬆️ **This is the AI-ONLY strategy above** - Notice how it focuses purely on results without considering broader implications"
                #     )
                # elif status_data["status"] == "completed":
                #     st.info(
                #         "⬆️ **This is the HUMAN-GUIDED strategy above** - See the comparison below"
                #     )

                if status_data["status"] == "awaiting_feedback":
                    st.subheader("💭 Human Feedback")
                    st.markdown(
                        "*Provide any feedback to see how it changes the AI's strategy*"
                    )

                    col_before, col_after = st.columns(2)

                    with col_before:
                        st.info("**🤖 AI-Only Strategy**")
                        st.write(
                            "Current proposal above shows AI working without human input"
                        )

                    with col_after:
                        st.success("**👤 Human-Guided Strategy**")
                        st.write("Provide feedback below to see how AI adapts")

                    st.markdown("---")

                    st.subheader("💡 Try These Feedback Examples")

                    feedback_examples = {
                        "🛡️ RBI/SEBI Compliance": "This strategy appears to violate RBI/SEBI guidelines and poses significant regulatory penalty risks. Please adopt a compliant approach that follows Indian financial regulations.",
                        "⚖️ Consumer Protection": "This could be considered misleading advertisement under the Consumer Protection Act. Please ensure transparent and honest messaging with proper disclaimers.",
                        "🎯 Cultural Sensitivity": "This approach may not align with Indian cultural values and sentiments. Please ensure respectful targeting that considers local customs and sensitivities.",
                        "📈 Long-term Brand Value": "This seems focused on short-term gains at the expense of brand reputation. Please consider long-term brand value and customer trust in the Indian market.",
                        "🏢 Corporate Ethics": "This doesn't align with our corporate values and responsible business practices. Please ensure ethical compliance with Indian business standards.",
                    }

                    selected_example = st.selectbox(
                        "Choose an example or write custom feedback:",
                        ["Custom Feedback"] + list(feedback_examples.keys()),
                    )

                    if selected_example != "Custom Feedback":
                        feedback_text = feedback_examples[selected_example]
                        st.text_area(
                            "Feedback Preview:",
                            feedback_text,
                            height=100,
                            disabled=True,
                        )

                        if st.button("🚀 Submit This Feedback", type="primary"):
                            with st.spinner(
                                "🤖 AI is revising strategy based on your feedback..."
                            ):
                                result = ui.submit_feedback(
                                    st.session_state.session_id, feedback_text
                                )
                                if result:
                                    st.success(
                                        "Strategy revised! See the difference below."
                                    )
                                    time.sleep(1)
                                    st.rerun()
                    else:
                        feedback_text = st.text_area(
                            "Your Custom Feedback:",
                            height=100,
                            placeholder="Enter any feedback about the AI's strategy. For example: concerns about ethics, compliance, targeting, messaging, etc.",
                        )

                        if st.button(
                            "🚀 Submit Feedback",
                            type="primary",
                            disabled=not feedback_text,
                        ):
                            with st.spinner(
                                "🤖 AI is revising strategy based on your feedback..."
                            ):
                                result = ui.submit_feedback(
                                    st.session_state.session_id, feedback_text
                                )
                                if result:
                                    st.success(
                                        "Strategy revised! See the difference below."
                                    )
                                    time.sleep(1)
                                    st.rerun()

                elif status_data["status"] == "completed":
                    st.success("🎉 **Human-in-the-Loop Demonstration Complete!**")

                    st.subheader("📊 Before vs After Comparison")

                    col_before, col_after = st.columns(2)

                    with col_before:
                        st.error("**🤖 BEFORE: AI-Only Strategy**")
                        st.markdown("*Without human oversight*")
                        if status_data["initial_proposal"]:
                            st.write(status_data["initial_proposal"])
                        else:
                            st.write("Original strategy not available or not stored.")

                    with col_after:
                        st.success("**👤 AFTER: Human-Guided Strategy**")
                        st.markdown("*With human feedback incorporated*")
                        st.write(status_data["current_proposal"])

                    if status_data["feedback_history"]:
                        st.subheader("💭 Human Feedback That Made the Difference")
                        st.info(
                            f"**Your Feedback:** {status_data['feedback_history'][0]}"
                        )

                        st.subheader("🎯 Key Takeaway")
                        st.success(
                            """
                        **Same AI, Same Product, Completely Different Result**
                        
                        This demonstrates why human oversight is essential for responsible AI deployment in Indian markets. 
                        The AI didn't become smarter - it just received human guidance about compliance with Indian regulations, 
                        cultural values, and ethical business practices.
                        """
                        )

                    st.markdown("---")
                    col_reset, col_try = st.columns(2)
                    with col_reset:
                        if st.button("🔄 Try Same Scenario Again"):
                            st.session_state.session_id = None
                            st.session_state.campaign_data = None
                            st.rerun()
                    with col_try:
                        if st.button("🎭 Try Different Scenario"):
                            st.session_state.session_id = None
                            st.session_state.campaign_data = None
                            st.rerun()


if __name__ == "__main__":
    main()
