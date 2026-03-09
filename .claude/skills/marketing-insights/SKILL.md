# Marketing Insights Analyst

## Purpose
Use this skill for the AI-Driven Marketing Workflow Analytics Prototype.

This skill helps analyze CSV-based campaign data and convert raw marketing metrics into business-friendly insights. It is designed for a Python-only Streamlit prototype that models the workflow from campaign planning and simulated publishing to engagement, leads, conversions, funnel analysis, and recommendations.

## Important project constraints
- This project is Python-only
- Use `.py` files only
- Do not use notebooks
- Data comes from CSV files
- Publishing is simulated, not live
- No real social media API integrations
- No real CRM integrations
- No authentication
- No live automation workflows in v1

## Project files
The project uses:
- `app.py`
- `data/campaigns.csv`
- `data/engagement.csv`
- `data/leads.csv`
- `utils/data_loader.py`
- `utils/metrics.py`
- `utils/insights.py`
- `utils/claude_layer.py`
- `pages/1_Overview.py`
- `pages/2_Channel_Performance.py`
- `pages/3_Content_Analysis.py`
- `pages/4_Funnel_Analysis.py`
- `pages/5_Claude_Insights.py`

## Datasets

### campaigns.csv
Columns:
- campaign_id
- campaign_name
- platform
- content_type
- topic
- audience_segment
- publish_date
- status

Purpose:
Represents campaign planning and simulated publishing.

A campaign with `status = Published` is treated as already published.

### engagement.csv
Columns:
- campaign_id
- impressions
- clicks
- likes
- comments
- shares

Purpose:
Represents post-publication engagement.

### leads.csv
Columns:
- campaign_id
- leads_generated
- qualified_leads
- conversions

Purpose:
Represents business outcomes from campaigns.

## Workflow modeled by the app

### 1. Campaign planning
Campaigns are defined using metadata such as:
- platform
- content type
- audience segment
- topic
- publish date

### 2. Publishing
Publishing is simulated in the data.
There is no real publishing system.
The app should treat campaigns marked as Published as already live.

### 3. Engagement tracking
The app analyzes:
- impressions
- clicks
- likes
- comments
- shares

### 4. Lead generation
The app analyzes:
- leads generated
- qualified leads
- conversions

### 5. Funnel analysis
The app analyzes progression through:
- impressions
- clicks
- leads_generated
- qualified_leads
- conversions

### 6. Executive recommendations
The app should generate business-facing observations and next steps.

## What this skill should do

### Campaign classification
Classify campaigns into business-relevant buckets such as:
- Awareness
- Consideration
- Conversion

Also infer likely campaign intent:
- brand visibility
- education
- product interest
- event registration
- lead generation

### Platform analysis
Explain:
- which platform performs best for reach
- which platform performs best for clicks
- which platform performs best for leads
- which platform performs best for conversion efficiency

### Content analysis
Explain:
- which content type creates the most awareness
- which content type drives the best lead quality
- which content type should be scaled

### Funnel diagnostics
Identify:
- the biggest funnel drop-off
- what it likely means
- what should be improved next

### Founder-ready summaries
Translate raw metrics into concise business summaries.

Tone:
- clear
- direct
- actionable
- executive-friendly

## Preferred logic
- Start from actual CSV metrics
- Compare platforms separately from content types
- Distinguish awareness success from conversion success
- Do not assume that high impressions means best performance
- Give credit to high-conversion, high-quality channels even if reach is lower
- Keep outputs grounded in the data

## Recommendation rules
Use logic like this:

- If impressions are high but CTR is low, recommend improving messaging or creative
- If clicks are high but leads are low, recommend improving CTA or landing alignment
- If qualified lead rate is high, highlight that content/channel as high-intent
- If Email converts better than social, position Email as a stronger lower-funnel channel
- If LinkedIn has higher reach, position it as a stronger awareness channel
- If Event Promotion generates more leads, suggest scaling event-style campaigns
- If Case Study produces stronger qualified leads, suggest using it deeper in the funnel

## Output format
Use this structure when generating summaries:

### Executive Summary
2-4 sentences summarizing the most important findings.

### What is Working
- 2 to 4 bullets

### What is Underperforming
- 2 to 4 bullets

### Recommended Next Steps
- 3 to 5 bullets

## Guardrails
- Do not claim live publishing exists
- Do not claim CRM integration exists
- Do not invent backend workflows that are not implemented
- Treat publishing as simulated unless the code explicitly changes
- Be honest if insight generation is rule-based rather than live LLM-powered
- Keep outputs tied to actual campaign/platform/content/funnel behavior

## Example tasks this skill should support
- Analyze the merged campaign data and summarize strongest channels
- Classify campaigns into funnel stages
- Identify the biggest funnel bottleneck
- Generate founder-friendly recommendations
- Explain which content type is strongest for awareness vs conversion
- Summarize why one platform should be scaled and another optimized