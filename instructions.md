# AI-Driven Marketing Workflow Analytics Prototype

## Overview

A Python-only Streamlit prototype that models a full marketing analytics workflow:

1. Campaign planning via CSV metadata
2. Simulated publishing (status = Published)
3. Engagement tracking (impressions, clicks, likes, comments, shares)
4. Lead generation (leads, qualified leads, conversions)
5. Funnel analysis (impressions → clicks → leads → qualified leads → conversions)
6. Claude-style intelligence layer with plain-English insights

## Setup

### 1. Create virtual environment

```bash
python -m venv venv
```

### 2. Activate

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Run the App

```bash
streamlit run app.py
```

The app opens in your browser. Use the sidebar to filter by platform, content type, and audience segment. Navigate between pages using the sidebar menu.

## Pages

| Page | What It Shows |
|------|--------------|
| Home | Quick snapshot with KPI cards and sidebar filters |
| Overview | Full KPI dashboard with campaign distribution charts |
| Channel Performance | Platform comparison: engagement, CTR, conversion rate |
| Content Analysis | Content type breakdown: leads, conversions, rankings |
| Funnel Analysis | Full funnel chart with stage-to-stage drop-off analysis |
| Claude Insights | Campaign classification, summaries, and executive recommendations |

## Project Structure

```
marketing_analytics/
├── app.py                         # Main entry point
├── requirements.txt               # Python dependencies
├── instructions.md                # This file
├── data/
│   ├── campaigns.csv              # Campaign metadata
│   ├── engagement.csv             # Post-publish engagement metrics
│   └── leads.csv                  # Lead and conversion outcomes
├── utils/
│   ├── __init__.py
│   ├── data_loader.py             # CSV loading and merging
│   ├── metrics.py                 # KPI calculations and aggregation
│   ├── insights.py                # Rule-based business insights
│   └── claude_layer.py            # Simulated Claude intelligence layer
└── pages/
    ├── 1_Overview.py
    ├── 2_Channel_Performance.py
    ├── 3_Content_Analysis.py
    ├── 4_Funnel_Analysis.py
    └── 5_Claude_Insights.py
```

## Constraints

- Python-only (no notebooks)
- CSV-based dummy data only (no live APIs)
- Publishing is simulated through campaign metadata
- No CRM, authentication, or social media integrations
- Claude layer is rule-based, not connected to an LLM API
