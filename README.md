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
├── main.py                  # FastAPI application (backend)
├── models.py                # Pydantic models and data structures
├── services.py              # OpenAI service and business logic
├── workflow.py              # LangGraph workflow definitions
├── streamlit_app.py         # Streamlit UI (frontend)
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

```bash
python main.py
```
- **Main API**: http://127.0.0.1:8000
- **Interactive Docs**: http://127.0.0.1:8000/docs
