# Marketing Analytics Dashboard — Complete Guide

**A full guide for anyone who uses, reviews, or works with this dashboard — whether you're a business leader, marketer, or developer.**

---

## Table of Contents

1. [What Is This Dashboard?](#1-what-is-this-dashboard)
2. [How to Use the Dashboard](#2-how-to-use-the-dashboard)
3. [Understanding the Data](#3-understanding-the-data)
4. [Every Page Explained in Detail](#4-every-page-explained-in-detail)
5. [Understanding the Metrics](#5-understanding-the-metrics)
6. [The Filters — How They Work](#6-the-filters--how-they-work)
7. [The Ask AI Chatbot](#7-the-ask-ai-chatbot)
8. [Technical Architecture (For Developers)](#8-technical-architecture-for-developers)
9. [Project File Structure](#9-project-file-structure)
10. [Setup and Configuration](#10-setup-and-configuration)

---

## 1. What Is This Dashboard?

### In Plain Language

This is a **marketing analytics dashboard** — a web application that helps you understand how your marketing campaigns are performing. It shows you:

- **How many people saw your content** (impressions)
- **How many people clicked** (clicks)
- **How many people became leads** (people who gave you their contact info)
- **How many people became customers** (conversions)

The dashboard breaks this down by **where** you published (LinkedIn, Instagram, Email, Website), **what type** of content you used (thought leadership posts, case studies, event promotions, etc.), and **who** you targeted (HR teams, startup founders, enterprise buyers, etc.).

### Who Is It For?

- **Marketing managers** — to see which channels and content types work best
- **Executives and founders** — to get a quick snapshot of campaign performance
- **Content strategists** — to decide what to create more of
- **Anyone** who needs to answer: "Is our marketing working? Where should we invest more?"

### What Makes It Special?

1. **No external connections** — All data comes from three simple spreadsheet files. No databases, no live API connections. Everything is self-contained.

2. **Built-in intelligence** — The dashboard automatically classifies your campaigns, finds problems in your funnel, and suggests what to do next. This is done with rules, not AI — so it's fast and consistent.

3. **Ask AI feature** — You can type questions in plain English (e.g., "Which platform generates the most leads?") and get answers. This uses OpenAI's GPT model and requires an API key to work.

4. **Filters on every page** — You can narrow down the view to specific platforms, content types, or audience segments and see how the numbers change.

---

## 2. How to Use the Dashboard

### First Time You Open It

When you open the dashboard, you see:

1. **A navigation bar at the top** — With links: Home, Overview, Channels, Content, Funnel, Insights, Audience, and **Ask AI** (the green button on the right).

2. **The Home page** — Which shows a quick summary of your key numbers and a few charts.

### Moving Between Pages

- **Click any link** in the top navigation bar to go to that section.
- **Ask AI** is the green button — it opens a chat where you can ask questions about your data.
- The **Marketing Analytics** text on the far left is the app title, not a link.

### Pages That Have Filters

These pages have a **Filters** panel on the right side:

- Overview  
- Channels  
- Content  
- Funnel  
- Insights  
- Audience  

**Home** and **Ask AI** do not have filters. Home shows everything; Ask AI uses all data when answering.

### Using the Filters

Each filter is a dropdown where you can select one or more options:

- **Platform** — LinkedIn, Instagram, Email, Website (select which channels to include)
- **Content Type** — Thought Leadership, Educational Post, Product Highlight, Event Promotion, Case Study (select which content formats to include)
- **Audience Segment** — L&D Leaders, Startup Founders, HR Teams, Enterprise Buyers, Decision Makers (select which target audiences to include)

By default, **all options are selected**. When you remove a checkmark, that data is excluded from the charts and numbers on that page. The page updates immediately.

---

## 3. Understanding the Data

### Where Does the Data Come From?

The dashboard reads from **three CSV files** (spreadsheets) stored in the `data` folder:

1. **campaigns.csv** — A list of every marketing campaign, with details like name, platform, content type, audience, and publish date.
2. **engagement.csv** — For each campaign: how many impressions, clicks, likes, comments, and shares it got.
3. **leads.csv** — For each campaign: how many leads, qualified leads, and conversions it generated.

These three files are **joined together** using the campaign ID, so each campaign has its full story: what it was, where it ran, how it performed, and what it produced.

### What Each Data File Contains (In Detail)

#### campaigns.csv (48 campaigns)

| Column | What It Means |
|--------|---------------|
| **campaign_id** | A unique code for each campaign (e.g., C001, C002). |
| **campaign_name** | The name of the campaign (e.g., "AI Learning Launch", "Webinar Invite HR"). |
| **platform** | Where the campaign was published: **LinkedIn**, **Instagram**, **Email**, or **Website**. |
| **content_type** | The format of the content: **Thought Leadership** (opinion pieces, industry insights), **Educational Post** (how-to, tips), **Product Highlight** (feature demos, product info), **Event Promotion** (webinars, workshops, invites), or **Case Study** (customer success stories). |
| **topic** | The subject matter (e.g., "AI in Learning", "Marketing Automation"). |
| **audience_segment** | Who the campaign targeted: **L&D Leaders** (Learning & Development), **Startup Founders**, **HR Teams**, **Enterprise Buyers**, or **Decision Makers**. |
| **publish_date** | When the campaign was published (dates in March–April 2026). |
| **status** | Always "Published" — meaning the campaign has gone live. |

#### engagement.csv (48 rows, one per campaign)

| Column | What It Means |
|--------|---------------|
| **campaign_id** | Links to the campaign. |
| **impressions** | How many times the content was displayed (shown on screen). This is "reach" — how many people could have seen it. |
| **clicks** | How many times someone clicked on the content (e.g., a link, a CTA button). |
| **likes** | Social media likes or reactions. (Email campaigns have 0 — email doesn't have likes.) |
| **comments** | Social media comments. (Email campaigns have 0.) |
| **shares** | Social media shares. (Email campaigns have 0.) |

#### leads.csv (48 rows, one per campaign)

| Column | What It Means |
|--------|---------------|
| **campaign_id** | Links to the campaign. |
| **leads_generated** | How many people gave you their contact information (e.g., signed up, filled a form). |
| **qualified_leads** | How many of those leads met your qualification criteria (e.g., budget, authority, need). |
| **conversions** | How many of those leads became customers (signed, purchased, etc.). |

### The Marketing Funnel (Why It Matters)

The dashboard uses a **funnel** model. Think of it like a pipe:

1. **Impressions** — Content is shown to many people (top of funnel).
2. **Clicks** — Some of those people click (they're interested).
3. **Leads** — Some of those who clicked give you their info (they're engaged).
4. **Qualified Leads** — Some of those leads meet your criteria (they're serious).
5. **Conversions** — Some of those qualified leads become customers (bottom of funnel).

At each step, some people drop off. The dashboard helps you see **where** the biggest drop-off happens so you can fix it.

---

## 4. Every Page Explained in Detail

### Home Page

**What you see:** The first screen when you open the dashboard. No filters — it shows everything.

**Layout:** Full width. A row of key numbers at the top, then charts below.

#### Section 1: Key Metrics (6 cards in a row)

| Metric | What It Means |
|--------|---------------|
| **Campaigns** | Total number of marketing campaigns in the data. |
| **Impressions** | Total times your content was displayed across all campaigns. |
| **Clicks** | Total clicks across all campaigns. |
| **CTR** | Click-Through Rate — the percentage of people who saw your content and clicked. Formula: (clicks ÷ impressions) × 100. Higher is better. |
| **Conversions** | Total number of people who became customers. |
| **Conv. Rate** | Conversion Rate — the percentage of leads who became customers. Formula: (conversions ÷ leads) × 100. Higher is better. |

#### Section 2: Impressions by Platform (horizontal bar chart)

Shows which channel (LinkedIn, Instagram, Email, Website) delivered the most impressions. The longer the bar, the more people saw content on that channel. This answers: "Where are we reaching the most people?"

#### Section 3: Marketing Funnel (funnel-shaped chart)

A visual funnel with five stages: Impressions → Clicks → Leads → Qualified Leads → Conversions. Each stage shows the number and what percentage of the original impressions made it that far. You can see where the biggest drop-off occurs.

#### Section 4: Campaigns by Content Type (donut chart)

Shows how your campaigns are distributed across content types (Thought Leadership, Educational Post, Product Highlight, Event Promotion, Case Study). Answers: "What formats are we using most?"

#### Section 5: Leads by Platform (vertical bar chart)

Shows which platform generated the most leads. Answers: "Which channel is bringing us the most potential customers?"

#### Section 6: Conversion Rate by Platform (vertical bar chart)

Shows which platform has the highest conversion rate (leads turning into customers). Answers: "Which channel converts best?"

---

### Overview Page

**What you see:** A detailed KPI dashboard with filters on the right.

**Layout:** Main content on the left (about 75% width), filters on the right (about 25% width).

#### Section 1: Campaign Overview (heading)

#### Section 2: First Row of Metrics (4 cards)

| Metric | What It Means |
|--------|---------------|
| **Total Campaigns** | Number of campaigns (filtered if you changed filters). |
| **Total Impressions** | Total impressions for the filtered data. |
| **Total Clicks** | Total clicks for the filtered data. |
| **CTR** | Click-through rate for the filtered data. |

#### Section 3: Second Row of Metrics (4 cards)

| Metric | What It Means |
|--------|---------------|
| **Total Leads** | Total leads generated. |
| **Qualified Leads** | Total qualified leads. |
| **Total Conversions** | Total conversions. |
| **Conversion Rate** | Conversion rate for the filtered data. |

#### Section 4: Campaigns by Platform (bar chart)

Shows how many campaigns you ran on each platform. Uses filtered data.

#### Section 5: Campaigns by Content Type (bar chart)

Shows how many campaigns you ran for each content type. Uses filtered data.

**Why use this page:** When you want to see how the numbers change when you focus on specific platforms, content types, or audiences. For example: "What are our numbers if we only look at LinkedIn and Email?"

---

### Channels Page (Channel Performance)

**What you see:** A comparison of how each marketing channel (platform) performs.

**Layout:** Main content left, filters right.

#### Section 1: Engagement & Leads by Platform (grouped bar chart)

Three bars per platform: **Impressions** (blue), **Clicks** (orange), **Leads** (green). Lets you compare reach, engagement, and lead generation side by side for LinkedIn, Instagram, Email, and Website.

#### Section 2: CTR by Platform (horizontal bar chart)

Shows click-through rate for each platform, sorted from lowest to highest. Answers: "Which channel gets the most clicks relative to views?"

#### Section 3: Conversion Rate by Platform (horizontal bar chart)

Shows conversion rate for each platform, sorted from lowest to highest. Answers: "Which channel turns leads into customers best?"

#### Section 4: Platform Summary (data table)

A table with every metric for each platform: campaigns, impressions, clicks, leads, qualified leads, conversions, CTR (%), conversion rate (%), and lead rate (%). Lead rate = (leads ÷ clicks) × 100 — how well clicks turn into leads.

**Why use this page:** To decide where to invest more budget. For example: "LinkedIn has high reach but Email converts better — maybe we should shift some spend to Email."

---

### Content Page (Content Analysis)

**What you see:** A comparison of how each content type performs.

**Layout:** Main content left, filters right.

#### Section 1: Engagement Metrics by Content Type (grouped bar chart)

Three bars per content type: **Impressions**, **Clicks**, **Likes**. Shows which content formats get the most views, clicks, and social engagement.

#### Section 2: Leads Generated (horizontal bar chart)

Shows which content type generates the most leads. Answers: "What format brings in the most potential customers?"

#### Section 3: Conversions (horizontal bar chart)

Shows which content type generates the most conversions. Answers: "What format actually closes the most deals?"

#### Section 4: Content Type Performance Ranking (data table)

A table with: Content Type, Campaigns, CTR (%), Conv. Rate (%), Lead Rate (%). Sorted by conversion rate, highest first.

#### Section 5: Top-Performing Content Type (green success banner)

A highlighted message that says which content type has the highest conversion rate and how many campaigns it includes.

**Why use this page:** To decide what content to create more of. For example: "Event Promotion generates the most leads, but Case Study has the best conversion rate — we should do more case studies for bottom-funnel campaigns."

---

### Funnel Page (Funnel Analysis)

**What you see:** A deep dive into the marketing funnel and where people drop off.

**Layout:** Main content left, filters right.

#### Section 1: Marketing Funnel (funnel chart)

The same five-stage funnel as Home: Impressions → Clicks → Leads → Qualified Leads → Conversions. Shows values and percentage of initial. Uses filtered data.

#### Section 2: Stage-to-Stage Progression (data table)

For each transition (e.g., Impressions → Clicks), the table shows:

- **From** — The starting stage
- **To** — The next stage
- **Retained** — What percentage of people moved to the next stage (e.g., 4.2% of impressions became clicks)
- **Drop-off** — What percentage was lost (e.g., 95.8% did not click)
- **Volume Change** — The actual numbers (e.g., "500,000 → 21,000")

#### Section 3: Biggest Drop-Off (yellow warning banner)

A highlighted message that identifies the worst transition (e.g., "Impressions → Clicks: 95.8% loss, 479,000 volume lost") and says this is the primary area to optimize.

#### Section 4: Funnel by Platform (dropdown + funnel chart)

A dropdown lets you select **All** or a specific platform (LinkedIn, Instagram, Email, Website). The funnel chart below updates to show that platform's funnel. Answers: "Is the bottleneck the same across all channels, or is one channel worse?"

**Why use this page:** To find and fix the biggest leak in your pipeline. If most people drop off between Clicks and Leads, the problem is likely your landing page or CTA, not your ad creative.

---

### Insights Page (Claude-Style Intelligence Layer)

**What you see:** Automated analysis, recommendations, and two ways to consume the insights — visual (Interactive Dashboard) or text (Detailed Report).

**Layout:** Main content left, filters right. Two tabs at the top: **Interactive Dashboard** and **Detailed Report**.

---

#### Tab 1: Interactive Dashboard

##### Row 1: Executive Summary Metrics (6 cards in 2 rows of 3)

| Metric | What It Means |
|--------|---------------|
| **Best Reach Platform** | Which platform (LinkedIn, Instagram, Email, Website) has the most impressions. |
| **Best Conversion Platform** | Which platform has the highest conversion rate. |
| **Funnel Efficiency** | Overall: (conversions ÷ impressions) × 100. How efficient is the entire pipeline from view to customer? |
| **Biggest Drop-off Stage** | The stage where the funnel loses the most people (e.g., "Impressions"). |
| **Drop-off Volume Lost** | How many people were lost at that stage. |
| **Drop-off Percentage** | What percentage was lost. |

##### Platform: Reach vs Conversion (dual-axis bar chart)

Two bars per platform: **Impressions** (left axis) and **Conv. Rate (%)** (right axis). Shows that high reach doesn't always mean high conversion. A platform can have lots of impressions but a low conversion rate, or vice versa.

##### Content: Reach vs Conversion (dual-axis bar chart)

Same idea for content types: Impressions vs Conversion Rate. Shows which content drives visibility vs which drives conversions.

##### Campaign Classification (3 donut charts)

- **By Theme** — Awareness (top of funnel), Consideration (mid), Conversion (bottom). Based on content type.
- **By Intent** — Brand Visibility, Education, Product Interest, Event Registration, Trust Building. Based on content type.
- **By Funnel Stage** — Top-of-Funnel (Awareness), Mid-Funnel (Consideration), Bottom-of-Funnel (Conversion). Based on CTR and conversion rate thresholds per campaign.

##### What's Working (green success box)

Bullet points:
- Best reach platform
- Best conversion platform
- Best lead-generating content type
- Best converting content type

##### What Needs Attention (yellow warning box)

Bullet points:
- Biggest funnel drop-off and percentage
- Overall funnel efficiency
- Note that high-reach channels don't always convert best
- Note that some content drives awareness but underperforms on lead quality

##### Key Recommendations (5 blue info cards in a 3-column grid)

Actionable recommendations, for example:
- Double down on the best conversion platform for conversion campaigns
- Use the best reach platform as the primary awareness channel
- Scale the best converting content type
- Pair high-reach content with stronger CTAs
- Focus on reducing the biggest drop-off to improve end-to-end conversion

---

#### Tab 2: Detailed Report

For people who prefer reading over charts.

##### Campaign Classification (data table)

A table with every campaign and its: ID, Name, Platform, Content Type, Theme, Intent, Funnel Stage. You can see how each campaign is classified.

##### Platform Performance Summary (narrative text)

A few paragraphs explaining which platform is best for reach, which for conversion, which for leads, and whether there's a split (e.g., "LinkedIn for awareness, Email for conversion").

##### Content Performance Summary (narrative text)

A few paragraphs explaining which content type drives the most visibility, which has the best conversion rate, and which produces the strongest qualified leads.

##### Funnel Diagnosis (narrative text)

Explains the biggest funnel drop-off and what it likely means. For example:
- Impressions → Clicks: weak creative or poor targeting
- Clicks → Leads: landing page friction or misaligned expectations
- Leads → Qualified Leads: targeting too broad
- Qualified Leads → Conversions: sales process friction or pricing

##### Executive Recommendations (narrative text)

Five strategic recommendations in paragraph form, suitable for copying into a board deck or strategy doc.

##### Executive Summary Report (narrative text)

A short summary: total campaigns, impressions, conversions, overall funnel efficiency, and that performance varies across platforms and content types.

**Why use this page:** To get automated, data-backed recommendations without building reports manually. The Interactive Dashboard is for quick scanning; the Detailed Report is for deeper reading and sharing.

---

### Audience Page (Audience Segments)

**What you see:** A deep dive into which audience segments perform best.

**Layout:** Main content left, filters right.

#### Section 1: Top 3 Metric Cards

| Card | What It Shows |
|------|---------------|
| **Best Reach** | The audience segment (e.g., Decision Makers, Enterprise Buyers) that has the most impressions. |
| **Best Conversion Rate** | The segment with the highest conversion rate. |
| **Best Lead Quality** | The segment with the highest qualified lead rate (qualified ÷ leads × 100). |

#### Section 2: Engagement & Leads by Segment (grouped bar chart)

Three bars per segment: Impressions, Clicks, Leads. Shows which audiences you're reaching, engaging, and converting to leads.

#### Section 3: Conversion Rate by Segment (horizontal bar chart)

Which segments turn leads into customers best. Sorted from lowest to highest.

#### Section 4: Qualified Lead Rate by Segment (horizontal bar chart)

Which segments produce the highest-quality leads (more qualified, fewer unqualified). Sorted from lowest to highest.

#### Section 5: Segment vs Platform Performance (heatmap)

A grid: rows = audience segments, columns = platforms. Each cell shows the conversion rate for that segment on that platform. Darker green = higher conversion. Answers: "Does Enterprise Buyers convert better on LinkedIn or Email? Does Startup Founders perform better on Instagram or Website?"

#### Section 6: Segment Summary (data table)

A table with every metric per segment: Segment, Campaigns, Impressions, Clicks, Leads, Qualified, Conversions, CTR (%), Conv. Rate (%), Qual. Rate (%).

**Why use this page:** To decide which audiences to invest in. For example: "Enterprise Buyers convert best — we should run more campaigns targeting them. Startup Founders have high reach but low conversion — we may need different messaging."

---

### Ask AI Page (Chat)

**What you see:** A chat interface. A message history (if you've asked questions before) and an input box at the bottom.

**Layout:** Full width. No filters. The chatbot always uses all data when answering.

**How to use it:**

1. Type a question in the input box (e.g., "Which platform has the highest CTR?" or "Compare LinkedIn and Email for lead generation").
2. Press Enter or click Send.
3. The AI responds with an answer based on your campaign data.
4. You can ask follow-up questions — the chat remembers the conversation.

**What you can ask:**

- "Which campaign had the best conversion rate?"
- "How many leads did we get from LinkedIn?"
- "What should we prioritize next quarter?"
- "Compare Event Promotion vs Case Study content."

**Requirements:** The Ask AI feature uses OpenAI's GPT-4.1-mini model. You need to set the `OPENAI_API_KEY` environment variable with a valid OpenAI API key. Without it, you'll see an error when you try to ask a question.

**Safety:** The chatbot has guardrails to prevent misuse. It only answers questions about your marketing data. It will refuse off-topic questions or attempts to change its behavior.

---

## 5. Understanding the Metrics

### Core Metrics (Used Throughout the Dashboard)

| Metric | Formula | Plain-Language Meaning |
|--------|---------|------------------------|
| **CTR (Click-Through Rate)** | (clicks ÷ impressions) × 100 | Of everyone who saw your content, what percentage clicked? Higher = more engaging content or better targeting. |
| **Conversion Rate** | (conversions ÷ leads) × 100 | Of everyone who became a lead, what percentage became a customer? Higher = better lead quality or sales process. |
| **Lead Rate** | (leads ÷ clicks) × 100 | Of everyone who clicked, what percentage became a lead? Higher = better landing page or CTA. |
| **Qualified Rate** | (qualified leads ÷ leads) × 100 | Of everyone who became a lead, what percentage met your qualification criteria? Higher = better targeting or lead quality. |
| **Funnel Efficiency** | (conversions ÷ impressions) × 100 | Of everyone who saw your content, what percentage became a customer? The end-to-end efficiency of your pipeline. |
| **Drop-off %** | (current stage − next stage) ÷ current stage × 100 | What percentage of people left the funnel at this step? |
| **Retention %** | next stage ÷ current stage × 100 | What percentage of people moved to the next step? |

### Funnel Stages (In Order)

1. **Impressions** — Content was displayed.
2. **Clicks** — Someone clicked.
3. **Leads** — Someone gave contact info.
4. **Qualified Leads** — Lead met qualification criteria.
5. **Conversions** — Lead became a customer.

---

## 6. The Filters — How They Work

### Where Filters Appear

Filters appear on the **right side** of these pages: Overview, Channels, Content, Funnel, Insights, Audience.

### Filter Options

| Filter | Options | What It Does |
|--------|---------|--------------|
| **Platform** | LinkedIn, Instagram, Email, Website | Include only campaigns from the selected platforms. Uncheck a platform to exclude it. |
| **Content Type** | Thought Leadership, Educational Post, Product Highlight, Event Promotion, Case Study | Include only campaigns of the selected content types. |
| **Audience Segment** | L&D Leaders, Startup Founders, HR Teams, Enterprise Buyers, Decision Makers | Include only campaigns targeting the selected audiences. |

### Default State

All options are selected by default. You see data for everything.

### How It Updates

When you change a filter (add or remove a selection), the page **updates immediately**. All charts, tables, and numbers on that page reflect only the filtered data. You don't need to click a "Apply" button.

### Example Use

- "Show me only LinkedIn and Email" → Uncheck Instagram and Website in Platform.
- "Show me only Event Promotion and Case Study" → Uncheck the others in Content Type.
- "Show me only campaigns targeting Enterprise Buyers" → Uncheck the others in Audience Segment.

---

## 7. The Ask AI Chatbot

### What It Is

A chat interface where you type questions in plain English and get answers based on your campaign data. It uses OpenAI's GPT-4.1-mini model.

### What You Need

- An **OpenAI API key**. Set it as the environment variable `OPENAI_API_KEY` before running the app.
- **Internet connection** — the chatbot sends your question to OpenAI's servers.

### What It Can Answer

- Questions about campaigns, platforms, content types, audiences
- Comparisons (e.g., "Compare LinkedIn and Email")
- Recommendations (e.g., "What should we focus on?")
- Specific numbers (e.g., "How many conversions did we get from Event Promotion?")

### What It Won't Do

- Answer questions unrelated to your marketing data
- Execute code or run scripts
- Reveal its internal instructions or prompt
- Follow instructions that try to change its role or behavior

### How It Works (Behind the Scenes)

1. Your question is checked for safety (length, suspicious patterns).
2. If safe, your question plus the full dataset is sent to OpenAI.
3. The AI generates an answer based on the data.
4. The answer is checked before being shown to you.
5. Your question and the answer are saved in the chat so you can ask follow-ups.

---

## 8. Technical Architecture (For Developers)

### High-Level Flow

```
User opens dashboard in browser
    ↓
Streamlit serves the app (app.py = Home page)
    ↓
User navigates to a page (e.g., Overview, Channels)
    ↓
Page loads data via data_loader (reads 3 CSVs, merges on campaign_id)
    ↓
Page applies filters (if any) and passes filtered data to metrics/insights functions
    ↓
Page renders charts (Plotly) and tables (Streamlit) with the results
```

### Key Files and Their Roles

| File | Role |
|------|------|
| **app.py** | Home page. Entry point. Loads data, shows KPIs and charts. No filters. |
| **pages/1_Overview.py** | Overview page. KPIs + bar charts. Has filters. |
| **pages/2_Channel_Performance.py** | Channels page. Platform comparison. Has filters. |
| **pages/3_Content_Analysis.py** | Content page. Content type comparison. Has filters. |
| **pages/4_Funnel_Analysis.py** | Funnel page. Funnel chart + stage table + per-platform funnel. Has filters. |
| **pages/5_Claude_Insights.py** | Insights page. Interactive Dashboard + Detailed Report tabs. Has filters. |
| **pages/6_Chat.py** | Ask AI page. Chat interface. No filters. Uses full data. |
| **pages/7_Audience_Segments.py** | Audience page. Segment analysis + heatmap. Has filters. |
| **utils/data_loader.py** | Loads campaigns.csv, engagement.csv, leads.csv. Merges on campaign_id. |
| **utils/metrics.py** | KPI formulas (CTR, conversion rate, lead rate) and aggregations (platform_metrics, content_type_metrics, segment_metrics, funnel_metrics, summarize_kpis). |
| **utils/insights.py** | Rule-based insights: get_best_platform, get_best_content_type, get_biggest_dropoff, get_recommendations. |
| **utils/claude_layer.py** | Campaign classification (theme, intent, funnel stage) and narrative summaries (platform, content, funnel diagnosis, founder recommendations). |
| **utils/chatbot.py** | OpenAI integration. System prompt, input sanitization, output validation, query_llm. |
| **utils/filters.py** | Renders Platform, Content Type, Audience Segment multiselects. Returns filtered DataFrame. |
| **utils/layout.py** | Renders top nav bar, applies global CSS, setup_page(). |

### Data Flow

1. `load_merged_data()` in data_loader.py reads all three CSVs and joins them on `campaign_id`.
2. `apply_filters(container)` in filters.py loads the merged data, renders the filter widgets in the given container, and returns a filtered DataFrame based on user selections.
3. Each page passes the (filtered) DataFrame to the relevant functions in metrics.py, insights.py, and claude_layer.py.
4. Results are rendered as Streamlit components (st.metric, st.plotly_chart, st.dataframe, etc.).

---

## 9. Project File Structure

```
marketing_analytics/
├── .streamlit/
│   └── config.toml              # Theme colors, hot reload settings
├── data/
│   ├── campaigns.csv            # 48 campaigns: name, platform, content type, audience, date
│   ├── engagement.csv           # Impressions, clicks, likes, comments, shares per campaign
│   └── leads.csv                # Leads, qualified leads, conversions per campaign
├── pages/
│   ├── 1_Overview.py            # KPI dashboard with filters
│   ├── 2_Channel_Performance.py # Platform comparison
│   ├── 3_Content_Analysis.py    # Content type analysis
│   ├── 4_Funnel_Analysis.py     # Funnel visualization and diagnosis
│   ├── 5_Claude_Insights.py     # Insights (Interactive Dashboard + Detailed Report)
│   ├── 6_Chat.py                # Ask AI chatbot
│   └── 7_Audience_Segments.py   # Audience segment deep-dive
├── utils/
│   ├── chatbot.py               # OpenAI API + guardrails
│   ├── claude_layer.py          # Campaign classification + narrative summaries
│   ├── data_loader.py           # CSV loading and merging
│   ├── filters.py               # Filter widgets
│   ├── insights.py              # Rule-based business insights
│   ├── layout.py                # Navigation bar + global CSS
│   └── metrics.py               # KPI formulas + aggregations
├── app.py                       # Home page (entry point)
├── requirements.txt             # Python dependencies
├── README.md                    # Setup and run instructions
└── PROJECT_DOCUMENTATION.md     # This file
```

---

## 10. Setup and Configuration

### Running the Dashboard Locally

1. Install Python 3.10 or higher.
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac/Linux)
4. Install dependencies: `pip install -r requirements.txt`
5. Set OpenAI API key (for Ask AI): `$env:OPENAI_API_KEY = "sk-..."` (PowerShell) or `export OPENAI_API_KEY="sk-..."` (Mac/Linux)
6. Run the app: `streamlit run app.py`
7. Open the URL shown (usually http://localhost:8501)

### Theme and Hot Reload

The `.streamlit/config.toml` file sets:

- **Theme** — Sea green (#2E8B57) as primary color, white background, light green for cards
- **Hot reload** — The app automatically refreshes when you save a file (for development)

### Environment Variables

| Variable | Required For | Purpose |
|----------|--------------|---------|
| `OPENAI_API_KEY` | Ask AI (Chat) page | Authenticates with OpenAI API. Without it, the Chat page will show an error when you ask a question. |

---

*This document was written to be useful for both non-technical readers (business users, marketers, executives) and technical readers (developers, analysts). If you have questions or find something unclear, please update this document or reach out to the project maintainer.*
