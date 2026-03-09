# AI-Driven Marketing Workflow Analytics

A Streamlit dashboard that models a full marketing analytics workflow — from campaign planning and simulated publishing to engagement tracking, lead generation, funnel analysis, and an AI-powered chatbot for querying your data.

## Prerequisites

- Python 3.10+
- An [OpenAI API key](https://platform.openai.com/api-keys)

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/niharikaarun1902/marketing_analytics.git
cd marketing_analytics
```

### 2. Create and activate a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your OpenAI API key

**Windows (PowerShell):**

```powershell
$env:OPENAI_API_KEY = "sk-your-key-here"
```

**macOS / Linux:**

```bash
export OPENAI_API_KEY="sk-your-key-here"
```

### 5. Run the app

```bash
streamlit run app.py
```

The app opens in your browser at `http://localhost:8501`.

## Pages

| Page | Description |
|------|-------------|
| Home | Quick snapshot with KPI cards and sidebar filters |
| Overview | Full KPI dashboard with campaign distribution charts |
| Channel Performance | Platform comparison — engagement, CTR, conversion rate |
| Content Analysis | Content type breakdown — leads, conversions, rankings |
| Funnel Analysis | Full funnel chart with stage-to-stage drop-off analysis |
| Claude Insights | Campaign classification, summaries, and executive recommendations |
| Chat | AI chatbot (GPT-4.1-mini) for natural-language questions about the data |

## Project Structure

```
marketing_analytics/
├── app.py                         # Main entry point
├── requirements.txt               # Python dependencies
├── data/
│   ├── campaigns.csv              # Campaign metadata
│   ├── engagement.csv             # Post-publish engagement metrics
│   └── leads.csv                  # Lead and conversion outcomes
├── utils/
│   ├── __init__.py
│   ├── data_loader.py             # CSV loading and merging
│   ├── metrics.py                 # KPI calculations and aggregation
│   ├── insights.py                # Rule-based business insights
│   ├── claude_layer.py            # Rule-based intelligence layer
│   ├── chatbot.py                 # OpenAI integration and guardrails
│   └── filters.py                 # Sidebar filter widgets
└── pages/
    ├── 1_Overview.py
    ├── 2_Channel_Performance.py
    ├── 3_Content_Analysis.py
    ├── 4_Funnel_Analysis.py
    ├── 5_Claude_Insights.py
    └── 6_Chat.py
```

## Data

The app uses three CSV files in `data/`, all joined on `campaign_id`:

- **campaigns.csv** — campaign name, platform, content type, topic, audience segment, publish date, status
- **engagement.csv** — impressions, clicks, likes, comments, shares
- **leads.csv** — leads generated, qualified leads, conversions

## Chatbot

The Chat page lets you ask natural-language questions about the campaign data. It uses OpenAI's GPT-4.1-mini model with the full dataset included as context.

The chatbot includes prompt injection guardrails:
- System prompt hardening with strict role boundaries
- Input sanitization that blocks common injection patterns
- Output validation that detects prompt leakage

## Constraints

- Python-only (no notebooks)
- CSV-based sample data (no live APIs)
- Publishing is simulated through campaign metadata
- No CRM, authentication, or social media integrations
