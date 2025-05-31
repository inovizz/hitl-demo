# Marketing Campaign HITL (Human-in-the-Loop) Workflow

A FastAPI application demonstrating the critical importance of human oversight in AI-driven marketing campaigns using LangGraph and OpenAI.

## 🎯 Project Overview

This application showcases how AI-generated marketing strategies can be problematic without human guidance and how human intervention leads to better, more ethical, and brand-safe outcomes.

### Key Demonstrations

- **Brand Safety**: How AI might suggest risky messaging without human oversight
- **Cultural Sensitivity**: International campaign considerations across diverse markets  
- **Competitive Intelligence**: Strategic positioning with competitive analysis
- **Executive Escalation**: High-stakes decisions requiring senior approval
- **Regulatory Compliance**: Ensuring campaigns meet advertising standards

## 🏗️ Project Structure

```
marketing-campaign-hitl/
│
├── README.md                 # This documentation
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
│
├── main.py                  # FastAPI application (backend)
├── models.py                # Pydantic models and data structures
├── services.py              # OpenAI service and business logic
├── workflow.py              # LangGraph workflow definitions
├── demo.py                  # Command-line demonstration script
├── streamlit_app.py         # Streamlit UI (frontend)
└── run_app.py               # Launcher for both backend and frontend
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- pip package manager

### Installation

1. **Clone or create the project directory:**
```bash
mkdir marketing-campaign-hitl
cd marketing-campaign-hitl
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables (REQUIRED):**
```bash
cp .env.example .env
```
Edit the `.env` file and add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-actual-openai-api-key-here
```

**Important:** You must have a valid OpenAI API key for the application to work. Get one from: https://platform.openai.com/api-keys

### Running the Application

#### Option 1: Interactive Streamlit UI (Recommended)
```bash
python run_app.py
```
This starts both the FastAPI backend and Streamlit frontend automatically.
- **Streamlit UI**: http://localhost:8501
- **API Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

#### Option 2: FastAPI Only
```bash
python main.py
```
- **Main API**: http://127.0.0.1:8000
- **Interactive Docs**: http://127.0.0.1:8000/docs

#### Option 3: Manual Startup
```bash
# Terminal 1 - Start FastAPI backend
uvicorn main:app --reload

# Terminal 2 - Start Streamlit frontend  
streamlit run streamlit_app.py
```

## 🖥️ Streamlit UI Features

The interactive Streamlit interface provides:

### 🎛️ Configuration Panel
- **Campaign Setup**: Product name, goals, and budget configuration
- **Quick Scenarios**: Pre-configured test scenarios for different use cases

### 📊 Campaign Management  
- **Real-time Status**: Live workflow status and iteration tracking
- **Visual Proposal Display**: Clean formatting of AI-generated strategies
- **Interactive Feedback**: Guided feedback options with templates

### 💬 Smart Feedback System
- **Feedback Types**: Request info, revise strategy, approve, reject, escalate
- **Template Suggestions**: Pre-built feedback for common scenarios
- **Custom Input**: Freeform feedback for specific situations

### 📈 Progress Tracking
- **Status Badges**: Visual workflow state indicators
- **Feedback History**: Complete audit trail of human inputs
- **Research Context**: Display of gathered information and analysis

## 🎮 Running Demonstrations

### Interactive Streamlit UI (Recommended)
1. **Start the application:** `python run_app.py`
2. **Open your browser:** http://localhost:8501
3. **Choose a scenario:**
   - **Brand Safety Test**: Potentially problematic loan app campaign
   - **Global Campaign**: International tea launch with cultural considerations
   - **B2B Software**: CRM competing against major players
   - **High Stakes**: $10M AI platform disruption campaign
4. **Interact with the workflow** using guided feedback options

**Note:** Ensure your `.env` file contains a valid `OPENAI_API_KEY` before starting.

### Command-Line Demo Script
```bash
python demo.py
```

This will prompt you for your OpenAI API key and let you choose from 5 scenarios:

1. **No Human Oversight** ❌ - Shows dangerous immediate approval
2. **Brand Safety Review** ✅ - Demonstrates thorough safety analysis  
3. **Cultural Sensitivity** 🌍 - International campaign review
4. **Competitive Intelligence** 🎯 - Strategic competitive analysis
5. **Executive Escalation** 🏢 - High-stakes decision escalation

### Manual API Testing

1. **Start a campaign:**
```bash
curl -X POST http://127.0.0.1:8000/start_campaign_workflow \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "EcoFresh Organic Smoothies",
    "campaign_goal": "Launch premium health-focused smoothie line",
    "total_budget": "$500,000"
  }'
```

2. **Submit feedback:**
```bash
curl -X POST http://127.0.0.1:8000/submit_campaign_feedback/{session_id} \
  -H "Content-Type: application/json" \
  -d '{"feedback": "request_info: brand safety concerns"}'
```

3. **Check status:**
```bash
curl http://127.0.0.1:8000/campaign_status/{session_id}
```

## 📋 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/start_campaign_workflow` | Initialize new campaign workflow |
| GET | `/campaign_status/{session_id}` | Get current campaign status |
| POST | `/submit_campaign_feedback/{session_id}` | Submit human feedback |
| GET | `/sessions` | List all active sessions |
| GET | `/health` | Health check endpoint |

## 💬 Feedback Commands

### Information Gathering
- `"request_info: brand safety concerns"` - Analyze reputation risks
- `"request_info: cultural implications"` - Review cultural sensitivity
- `"request_info: competitor strategies"` - Competitive intelligence
- `"request_info: regulatory compliance"` - Advertising standards review

### Strategy Revision  
- `"revise to prioritize brand safety over conversion rates"`
- `"revise to ensure cultural sensitivity across all markets"`
- `"revise to comply with advertising standards"`
- `"revise messaging to be more inclusive"`

### Approval/Rejection
- `"approve"` - Accept current proposal
- `"reject"` - Reject current proposal  
- `"escalate: requires CEO approval"` - Escalate decision

## 🧪 Example Scenarios

### Scenario 1: Brand Safety Check
```python
# Start campaign
response = start_campaign("EcoFresh Smoothies", "Health-focused launch", "$500K")

# Request safety analysis  
submit_feedback(session_id, "request_info: brand safety concerns and potential reputation risks")

# Revise based on findings
submit_feedback(session_id, "revise to ensure brand safety and eliminate misleading health claims")

# Approve refined strategy
submit_feedback(session_id, "approve")
```

### Scenario 2: Cultural Sensitivity
```python
# Start global campaign
response = start_campaign("Global Wellness Tea", "International launch", "$2M")

# Analyze cultural implications
submit_feedback(session_id, "request_info: cultural sensitivity for Asian, European, and American markets")

# Request cultural adaptation
submit_feedback(session_id, "revise to ensure cultural appropriateness across all target markets")

# Approve culturally-aware strategy  
submit_feedback(session_id, "approve")
```

## 🎯 Learning Outcomes

### Without Human Intervention
AI marketing strategies typically exhibit:
- **Conversion obsession** - Pure metric focus without brand consideration
- **Aggressive targeting** - Potentially invasive audience targeting
- **Claims inflation** - Exaggerated or unsubstantiated promises
- **Cultural blindness** - Missing cultural nuances and sensitivities
- **Short-term focus** - Immediate ROI over long-term brand health

### With Human Guidance  
Human oversight transforms campaigns through:
- **Brand alignment** - Consistency with brand values and positioning
- **Risk mitigation** - Identifying reputation and compliance risks
- **Cultural intelligence** - Adapting messaging for diverse audiences  
- **Stakeholder balance** - Considering all impacts, not just conversions
- **Strategic thinking** - Balancing short-term and long-term objectives

## 🔧 Technical Architecture

### Components
- **FastAPI**: RESTful API framework with automatic documentation
- **LangGraph**: Workflow orchestration for human-AI collaboration
- **OpenAI GPT-4**: Large language model for marketing strategy generation
- **Pydantic**: Data validation and serialization
- **Python**: Core application logic and business rules

### Workflow States
- `initializing` - Starting new campaign
- `pending_review` - Awaiting human feedback
- `requesting_info` - Gathering additional information
- `revising` - Updating strategy based on feedback
- `approved` - Final approval received
- `rejected` - Proposal rejected
- `escalated` - Escalated to senior leadership

## 🛟 Troubleshooting

### Common Issues

**OpenAI API Errors:**
- Ensure your `.env` file exists with a valid `OPENAI_API_KEY`
- Verify your API key is valid and has sufficient credits
- Check if you have access to GPT-4 model
- Ensure proper internet connectivity

**Import Errors:**
- Run `pip install -r requirements.txt` to install all dependencies
- Verify Python version is 3.8 or higher

**Port Already in Use:**
- Change the port in main.py: `uvicorn.run(app, host="0.0.0.0", port=8001)`
- Or kill the process using port 8000

**Session Not Found:**
- Sessions are stored in memory and reset when restarting the application
- For production, implement persistent storage

## 📝 License

This project is for educational and demonstration purposes. Please ensure compliance with OpenAI's usage policies when using their API.

## 🤝 Contributing

This is a POC/demo application. For improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For questions or issues:
- Check the interactive documentation at `/docs`
- Review the demo script examples
- Examine the console output for workflow debugging
