# Marketing Analytics Dashboard — Complete Project Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Data Layer](#data-layer)
4. [Utility Modules](#utility-modules)
5. [Pages — Detailed Breakdown](#pages--detailed-breakdown)
6. [AI Chatbot](#ai-chatbot)
7. [Theming and Styling](#theming-and-styling)
8. [Filters](#filters)
9. [Navigation System](#navigation-system)
10. [Configuration](#configuration)
11. [Full Project Structure](#full-project-structure)
12. [Metrics Reference](#metrics-reference)

---

## Project Overview

This is a **Streamlit-based marketing analytics dashboard** designed for founders, executives, and marketing teams to understand campaign performance end-to-end. It models a complete marketing workflow — from campaign publishing and engagement tracking to lead generation, funnel analysis, audience segmentation, and AI-powered intelligence.

**Key differentiators:**

- **No external databases or APIs** — all data lives in three CSV files, making it fully self-contained and portable.
- **Rule-based intelligence layer** — automated campaign classification, funnel diagnosis, and executive recommendations without requiring an LLM.
- **AI chatbot (GPT-4.1-mini)** — natural-language interface for querying the data, with three layers of prompt injection protection.
- **Audience segment deep-dive** — identifies which audience segments convert best and deserve more investment.
- **Interactive filters** — every analytics page supports real-time filtering by platform, content type, and audience segment.

**Tech stack:** Python, Streamlit, Pandas, Plotly, OpenAI API, NumPy.

---

## Architecture

The application follows a **multi-page Streamlit architecture** with shared utilities:

```
User's Browser
    │
    ▼
┌──────────────────────────────────┐
│  Streamlit App (app.py)          │  ← Entry point / Home page
│  ├── pages/1_Overview.py         │
│  ├── pages/2_Channel_Performance │
│  ├── pages/3_Content_Analysis    │
│  ├── pages/4_Funnel_Analysis     │
│  ├── pages/5_Claude_Insights     │
│  ├── pages/6_Chat.py             │
│  └── pages/7_Audience_Segments   │
└───────────┬──────────────────────┘
            │
            ▼
┌──────────────────────────────────┐
│  Utility Layer (utils/)          │
│  ├── layout.py     → Nav + CSS  │
│  ├── filters.py    → Filtering  │
│  ├── data_loader.py → CSV I/O   │
│  ├── metrics.py    → KPI math   │
│  ├── insights.py   → Rules      │
│  ├── claude_layer.py → AI rules │
│  └── chatbot.py    → OpenAI API │
└───────────┬──────────────────────┘
            │
            ▼
┌──────────────────────────────────┐
│  Data Layer (data/)              │
│  ├── campaigns.csv               │
│  ├── engagement.csv              │
│  └── leads.csv                   │
└──────────────────────────────────┘
```

**Data flow:** Every page calls `apply_filters()` which internally calls `load_merged_data()` → loads all three CSVs → joins them on `campaign_id` → applies user-selected filters → returns a filtered DataFrame that the page then passes to the relevant metric/insight functions.

---

## Data Layer

All data lives in `data/` as static CSV files. There are no live API connections, databases, or real-time feeds. The data is simulated to represent a realistic B2B SaaS marketing program.

### campaigns.csv (48 campaigns)

The core campaign metadata table. Each row is one marketing campaign.

| Column | Type | Description |
|--------|------|-------------|
| `campaign_id` | string | Unique identifier (C001–C048) |
| `campaign_name` | string | Descriptive name (e.g., "AI Learning Launch") |
| `platform` | string | Distribution channel: **LinkedIn**, **Instagram**, **Email**, **Website** |
| `content_type` | string | Format: **Thought Leadership**, **Educational Post**, **Product Highlight**, **Event Promotion**, **Case Study** |
| `topic` | string | Subject matter (e.g., "AI in Learning", "Marketing Automation") |
| `audience_segment` | string | Target audience: **L&D Leaders**, **Startup Founders**, **HR Teams**, **Enterprise Buyers**, **Decision Makers** |
| `publish_date` | string | Date published in DD-MM-YYYY format (March–April 2026) |
| `status` | string | Always "Published" (simulates post-publish analytics) |

**Why it exists:** Provides the dimensional context for every campaign — who it targets, where it runs, what format it takes. Every other table joins back to this through `campaign_id`.

### engagement.csv (48 rows)

Post-publish engagement metrics, one row per campaign.

| Column | Type | Description |
|--------|------|-------------|
| `campaign_id` | string | Foreign key to campaigns.csv |
| `impressions` | int | Total times the content was displayed (3,900–16,200) |
| `clicks` | int | Total click-throughs (250–670) |
| `likes` | int | Social likes/reactions (0 for Email campaigns) |
| `comments` | int | Social comments (0 for Email campaigns) |
| `shares` | int | Social shares (0 for Email campaigns) |

**Data patterns:**
- LinkedIn campaigns have the highest impressions (14,000–16,200) — positioned as the awareness channel.
- Email campaigns have 0 likes/comments/shares (email doesn't have social engagement) but high clicks relative to impressions — positioned as a high-intent channel.
- Instagram campaigns sit in the middle range for impressions (8,600–9,800).

### leads.csv (48 rows)

Lead generation and conversion outcomes, one row per campaign.

| Column | Type | Description |
|--------|------|-------------|
| `campaign_id` | string | Foreign key to campaigns.csv |
| `leads_generated` | int | Total leads captured (13–57) |
| `qualified_leads` | int | Leads that passed qualification criteria (6–24) |
| `conversions` | int | Leads that converted to customers (2–10) |

**Data patterns:**
- Email and Event Promotion campaigns generate the most leads (36–57) — high-intent channels.
- Website/Case Study campaigns have strong qualified-lead ratios — trust-building content.
- Instagram campaigns generate fewer leads but still contribute to the pipeline.

### How data is loaded

`utils/data_loader.py` handles all data I/O:

1. **`load_campaigns()`** — reads `campaigns.csv` and parses `publish_date` from DD-MM-YYYY to datetime.
2. **`load_engagement()`** — reads `engagement.csv` as-is.
3. **`load_leads()`** — reads `leads.csv` as-is.
4. **`load_merged_data()`** — calls all three loaders, performs two left joins on `campaign_id`, and returns a single 48-row DataFrame with all columns from all three files.

This merged DataFrame is the single source of truth used by every page and utility function.

---

## Utility Modules

### utils/metrics.py — KPI Calculations

All mathematical calculations live here. Every page imports from this module rather than computing metrics inline.

**Base formulas:**

| Function | Formula | Returns |
|----------|---------|---------|
| `calculate_ctr(clicks, impressions)` | (clicks / impressions) × 100 | float (%) |
| `calculate_conversion_rate(conversions, leads)` | (conversions / leads) × 100 | float (%) |
| `calculate_lead_rate(leads, clicks)` | (leads / clicks) × 100 | float (%) |

All three handle division-by-zero by returning 0.0.

**Aggregation functions:**

| Function | Groups By | Returns | Used On |
|----------|-----------|---------|---------|
| `summarize_kpis(df)` | (none — totals) | dict with 9 KPIs | Home, Overview |
| `platform_metrics(df)` | `platform` | DataFrame with per-platform metrics | Channels, Home, Insights |
| `content_type_metrics(df)` | `content_type` | DataFrame with per-content-type metrics | Content, Insights |
| `segment_metrics(df)` | `audience_segment` | DataFrame with per-segment metrics + `qualified_rate` | Audience |
| `funnel_metrics(df)` | (none — stages) | list of dicts (stage name + value) | Funnel, Home, Insights |

Each aggregation function sums all engagement and lead columns per group, then appends calculated rate columns (CTR, conversion rate, lead rate). `segment_metrics()` additionally computes `qualified_rate` (qualified_leads / leads_generated × 100).

### utils/insights.py — Rule-Based Business Insights

Deterministic logic that analyzes the data and produces actionable findings. No LLM is involved.

| Function | What It Does |
|----------|-------------|
| `get_best_platform(df)` | Returns a dict identifying the best platform for reach, clicks, leads, and conversion rate |
| `get_best_content_type(df)` | Same as above but for content types |
| `get_top_campaign(df)` | Returns the single campaign row with the most conversions |
| `get_biggest_dropoff(df)` | Finds the funnel stage transition with the largest percentage loss |
| `get_recommendations(df)` | Generates a list of recommendation strings based on conditional rules |

**Recommendation rules in `get_recommendations()`:**
- If a platform has above-median impressions but below-median CTR → "improve ad creative"
- If a platform has above-median clicks but below-median lead rate → "review CTAs and landing pages"
- If a platform has above-median conversion rate → "consider scaling budget"
- If a content type has >55% qualified-lead ratio → "use deeper in the funnel"
- If a content type has above-median impressions but below-median leads → "pair with stronger CTAs"
- If the biggest funnel drop-off exceeds 80% → flag as critical

### utils/claude_layer.py — Intelligence Classification Layer

Named "Claude-style" because it mimics the analytical reasoning of an AI assistant, but is entirely rule-based. No API calls.

**Campaign classification:**

| Function | Logic | Output |
|----------|-------|--------|
| `classify_campaign_theme(row)` | Maps `content_type` → Theme | "Awareness" (Thought Leadership, Educational Post), "Consideration" (Product Highlight), "Conversion" (Event Promotion, Case Study) |
| `classify_campaign_intent(row)` | Maps `content_type` → Intent | "Brand Visibility", "Education", "Product Interest", "Event Registration / Lead Generation", "Trust Building / Conversion" |
| `classify_funnel_stage(row)` | Uses CTR and conversion rate thresholds | "Bottom-of-Funnel" (conv rate > 30%), "Mid-Funnel" (CTR > 5%), "Top-of-Funnel" (default) |

**Summary generators:**

| Function | What It Produces |
|----------|-----------------|
| `summarize_platform_performance(df)` | Multi-sentence narrative about which platform is best for reach, conversion, and leads |
| `summarize_content_performance(df)` | Narrative about which content type drives the most visibility, conversions, and qualified leads |
| `identify_funnel_issue(df)` | Finds the biggest funnel drop-off and provides a contextual diagnosis with explanation and recommended fix |
| `generate_founder_recommendations(df)` | Five executive-level recommendations combining platform, content, and funnel insights |

**Funnel diagnosis detail:** `identify_funnel_issue()` maps each possible stage-to-stage drop-off to a specific explanation:
- Impressions → Clicks: weak creative or poor targeting
- Clicks → Leads: landing page friction or misaligned expectations
- Leads → Qualified Leads: targeting criteria too broad
- Qualified Leads → Conversions: sales process friction or pricing objections

### utils/chatbot.py — OpenAI Integration with Guardrails

Handles all communication with the OpenAI API (GPT-4.1-mini model) and implements a three-layer security system against prompt injection.

**Layer 1: System Prompt Hardening** (`_build_system_prompt()`)

The system prompt includes:
- A unique sentinel string (`MARKETING_ANALYTICS_SYSTEM_BOUNDARY`) that should never appear in output
- Explicit instructions to only answer marketing data questions
- Explicit instructions to never follow user-embedded instructions that attempt role changes
- The complete merged dataset as CSV (so the LLM can reference actual numbers)
- Formula definitions for CTR, conversion rate, lead rate, and funnel stages
- Recommendation logic rules matching the rule-based insights module

**Layer 2: Input Sanitization** (`sanitize_input()`)

Before any message reaches the LLM:
- Messages over 1,000 characters are rejected
- 15+ regex patterns detect common injection attempts:
  - "ignore previous instructions", "disregard your rules"
  - "you are now", "act as", "pretend to be"
  - "reveal your prompt", "show me your system prompt"
  - LLM-specific formatting markers (`[INST]`, `<<SYS>>`, `<system>`)

If any pattern matches, the function returns a refusal message and the LLM is never called.

**Layer 3: Output Validation** (`validate_response()`)

After the LLM responds:
- If any sentinel phrase from the system prompt appears in the output (indicating prompt leakage), the response is replaced with a safe error message
- Responses exceeding 3,000 characters are truncated with a note

**API setup:**
- `_get_client()` reads `OPENAI_API_KEY` from environment variables
- `query_llm()` prepends the system prompt, sends the full conversation history, and returns the validated response

### utils/filters.py — Interactive Filters

Renders three multiselect widgets that filter the merged dataset in real-time:

| Filter | Column | Options |
|--------|--------|---------|
| Platform | `platform` | LinkedIn, Instagram, Email, Website |
| Content Type | `content_type` | Thought Leadership, Educational Post, Product Highlight, Event Promotion, Case Study |
| Audience Segment | `audience_segment` | L&D Leaders, Startup Founders, HR Teams, Enterprise Buyers, Decision Makers |

All filters default to "all selected." The function accepts a `container` parameter so filters can be rendered in any Streamlit column or container (they appear in the right-side column on all analytics pages).

### utils/layout.py — Navigation and Global Styling

Manages the top navigation bar and dashboard-wide CSS.

**Navigation:** Renders a horizontal row of `st.page_link` buttons for all 8 pages. The "Ask AI" button (chat page) is visually highlighted with a green gradient background to distinguish it as a CTA.

**Global CSS applied to every page:**
- Hides the default Streamlit sidebar navigation
- Styles nav links with hover effects (green background, white text)
- Styles KPI metric cards with a green left border, light green background
- Applies consistent typography and spacing

---

## Pages — Detailed Breakdown

### Home (`app.py`)

**Purpose:** Executive snapshot — the first thing a user sees. Provides a high-level summary without requiring any navigation.

**Layout:** Full-width (no filters sidebar).

**Content:**

| Section | Visualization | Data Source | Why It's Here |
|---------|--------------|-------------|---------------|
| Key Metrics row | 6 `st.metric` cards | `summarize_kpis()` | Instant pulse check — campaigns, impressions, clicks, CTR, conversions, conversion rate |
| Impressions by Platform | Horizontal bar chart (Plotly) | `platform_metrics()` | Shows which channels drive the most visibility |
| Marketing Funnel | Funnel chart (Plotly) | `funnel_metrics()` | Visualizes the full pipeline from impressions to conversions with percentage drop at each stage |
| Campaigns by Content Type | Donut chart (Plotly) | Grouped count of `content_type` | Shows content mix distribution |
| Leads by Platform | Vertical bar chart (Plotly) | `platform_metrics()` | Compares lead volume across channels |
| Conversion Rate by Platform | Vertical bar chart (Plotly) | `platform_metrics()` | Compares conversion efficiency across channels |

**Why these specific charts:** The home page answers three executive questions: "How much activity do we have?" (KPIs), "Where are we reaching people?" (platform impressions), and "How efficient is our pipeline?" (funnel + conversion rates).

---

### Overview (`pages/1_Overview.py`)

**Purpose:** Detailed campaign-level KPI dashboard with filtering.

**Layout:** 3:1 columns (content left, filters right).

**Content:**

| Section | Visualization | Metrics Shown |
|---------|--------------|---------------|
| KPI row 1 | 4 metric cards | Total Campaigns, Total Impressions, Total Clicks, CTR |
| KPI row 2 | 4 metric cards | Total Leads, Qualified Leads, Total Conversions, Conversion Rate |
| Campaigns by Platform | Vertical bar chart | Count of campaigns per platform |
| Campaigns by Content Type | Vertical bar chart | Count of campaigns per content type |

**Populated by:** `summarize_kpis(filtered_df)` — all 9 KPIs are calculated from the filtered dataset. The bar charts use simple `groupby().count()` on the filtered data.

**Why it exists:** The Home page shows totals; the Overview page lets users slice by platform, content type, and audience segment using the filters to see how KPIs change for specific subsets.

---

### Channel Performance (`pages/2_Channel_Performance.py`)

**Purpose:** Compare marketing channel (platform) effectiveness across the full funnel.

**Layout:** 3:1 columns (content left, filters right).

**Content:**

| Section | Visualization | What It Shows |
|---------|--------------|---------------|
| Engagement & Leads by Platform | Grouped bar chart (3 bars per platform) | Impressions, Clicks, and Leads side by side for each platform |
| CTR by Platform | Horizontal bar chart (ranked) | Click-through rate for each platform, sorted ascending |
| Conversion Rate by Platform | Horizontal bar chart (ranked) | Conversion rate for each platform, sorted ascending |
| Platform Summary | Data table | All metrics per platform: campaigns, impressions, clicks, leads, qualified leads, conversions, CTR, conversion rate, lead rate |

**Populated by:** `platform_metrics(filtered_df)` which groups by `platform` and aggregates all engagement and lead columns, then calculates CTR, conversion rate, and lead rate.

**Why it exists:** Answers "Which channel should we invest more in?" by showing that high reach doesn't always mean high conversion. For example, LinkedIn may have the most impressions but Email may convert better — this page makes that visible.

---

### Content Analysis (`pages/3_Content_Analysis.py`)

**Purpose:** Evaluate which content formats (Thought Leadership, Case Study, etc.) are most effective.

**Layout:** 3:1 columns (content left, filters right).

**Content:**

| Section | Visualization | What It Shows |
|---------|--------------|---------------|
| Engagement Metrics by Content Type | Grouped bar chart (3 bars per type) | Impressions, Clicks, Likes per content type |
| Leads Generated | Horizontal bar chart | Lead volume per content type |
| Conversions | Horizontal bar chart | Conversion count per content type |
| Content Type Performance Ranking | Data table | Campaigns, CTR, conversion rate, lead rate — sorted by conversion rate descending |
| Top-performer callout | `st.success` banner | Highlights the content type with the highest conversion rate |

**Populated by:** `content_type_metrics(filtered_df)` which groups by `content_type` and computes the same aggregates and rates as `platform_metrics()`.

**Why it exists:** Helps content strategists decide what to produce more of. Event Promotion content may generate the most leads, but Case Study content may have the best conversion rate — this page surfaces those distinctions.

---

### Funnel Analysis (`pages/4_Funnel_Analysis.py`)

**Purpose:** Visualize and diagnose the marketing funnel from first impression to final conversion.

**Layout:** 3:1 columns (content left, filters right).

**Content:**

| Section | Visualization | What It Shows |
|---------|--------------|---------------|
| Marketing Funnel | Plotly Funnel chart | 5 stages: Impressions → Clicks → Leads → Qualified Leads → Conversions. Shows values and percentage of initial. |
| Stage-to-Stage Progression | Data table | For each transition: from stage, to stage, retention %, drop-off %, volume change |
| Biggest drop-off | `st.warning` banner | Identifies the worst transition (e.g., "Impressions → Clicks: 95.8% loss") |
| Funnel by Platform | Dropdown + Funnel chart | Select a platform to see its individual funnel shape |

**Populated by:** `funnel_metrics(filtered_df)` returns the five-stage funnel values. `get_biggest_dropoff(filtered_df)` identifies the critical transition.

**Why it exists:** The funnel is the single most important diagnostic tool. If impressions are high but conversions are low, this page pinpoints exactly where the pipeline breaks. The per-platform funnel dropdown reveals whether the bottleneck is universal or channel-specific.

---

### Claude Insights (`pages/5_Claude_Insights.py`)

**Purpose:** AI-powered (rule-based) intelligence layer that classifies campaigns, diagnoses issues, and generates executive recommendations.

**Layout:** 3:1 columns (content left, filters right). Content is split into two tabs.

#### Tab 1: Interactive Dashboard

| Section | Visualization | What It Shows |
|---------|--------------|---------------|
| Executive summary metrics | 6 metric cards (2 rows of 3) | Best reach platform, best conversion platform, funnel efficiency %, biggest drop-off stage, drop-off volume, drop-off % |
| Platform: Reach vs Conversion | Dual-axis grouped bar chart | Impressions (left axis) vs conversion rate % (right axis) per platform — reveals the reach-vs-efficiency tradeoff |
| Content: Reach vs Conversion | Dual-axis grouped bar chart | Same comparison for content types |
| Campaign Classification | 3 donut charts | Distribution by Theme (Awareness/Consideration/Conversion), Intent (Brand Visibility/Education/etc.), and Funnel Stage (Top/Mid/Bottom) |
| What's Working | `st.success` callout | Bullet points: best reach platform, best conversion platform, best lead-generating content, best converting content |
| What Needs Attention | `st.warning` callout | Bullet points: biggest drop-off, low overall efficiency, reach ≠ conversion disconnect |
| Key Recommendations | 5 `st.info` cards (3-column grid) | Actionable recommendations: scale best converter, use best reach channel for awareness, scale best content, add CTAs to high-reach content, fix biggest drop-off |

**Populated by:**
- `get_best_platform()`, `get_best_content_type()`, `get_biggest_dropoff()` from `insights.py`
- `platform_metrics()`, `content_type_metrics()` from `metrics.py`
- `classify_campaign_theme()`, `classify_campaign_intent()`, `classify_funnel_stage()` from `claude_layer.py`

#### Tab 2: Detailed Report

| Section | Content | Source Function |
|---------|---------|-----------------|
| Campaign Classification | Full table with campaign ID, name, platform, content type, theme, intent, funnel stage | `classify_campaign_theme()`, `classify_campaign_intent()`, `classify_funnel_stage()` applied row-by-row |
| Platform Performance Summary | Multi-paragraph narrative | `summarize_platform_performance()` |
| Content Performance Summary | Multi-paragraph narrative | `summarize_content_performance()` |
| Funnel Diagnosis | Contextual analysis with explanation | `identify_funnel_issue()` |
| Executive Recommendations | 5 strategic recommendations | `generate_founder_recommendations()` |
| Executive Summary Report | Narrative synthesis | Inline calculation combining all findings |

**Why it exists:** Not everyone reads charts. The Interactive Dashboard is for visual thinkers; the Detailed Report is for readers who want narrative summaries they can copy into board decks or strategy documents. Together they ensure insights are accessible regardless of consumption preference.

---

### Ask AI / Chat (`pages/6_Chat.py`)

**Purpose:** Natural-language interface for querying campaign data using OpenAI's GPT-4.1-mini.

**Layout:** Full-width (no filters — the chatbot sees all data).

**Content:**

| Element | Description |
|---------|-------------|
| Chat history | Displays all previous messages using `st.chat_message()` |
| Input box | `st.chat_input()` at the bottom of the page |
| AI responses | Streamed from GPT-4.1-mini with the full merged dataset as context |

**How it works:**

1. User types a question
2. `sanitize_input()` checks for injection patterns — if flagged, returns a refusal without calling the API
3. If safe, `query_llm()` sends the conversation history + system prompt (including full dataset) to OpenAI
4. Response is validated by `validate_response()` — checked for prompt leakage and length
5. Both user message and AI response are appended to `st.session_state["chat_history"]` for conversation continuity

**Error handling:** Catches `AuthenticationError` (bad API key), `RateLimitError`, `APIConnectionError`, and generic exceptions — each with a user-friendly message.

**Why it exists:** Dashboards answer pre-defined questions. The chatbot answers ad-hoc questions: "Which campaign had the best CTR?", "Compare LinkedIn and Email for lead generation", "What should I prioritize next quarter?" — things that would require custom code or manual data analysis without it.

---

### Audience Segments (`pages/7_Audience_Segments.py`)

**Purpose:** Deep-dive into which audience segments convert best and deserve more investment.

**Layout:** 3:1 columns (content left, filters right).

**Content:**

| Section | Visualization | What It Shows |
|---------|--------------|---------------|
| Top 3 metrics | Custom HTML cards | Best Reach segment, Best Conversion Rate segment, Best Lead Quality segment (uses custom HTML instead of `st.metric` to avoid text truncation with long segment names) |
| Engagement & Leads by Segment | Grouped bar chart (3 bars per segment) | Impressions, Clicks, Leads side by side for each audience segment |
| Conversion Rate by Segment | Horizontal bar chart (ranked) | Which segments turn leads into conversions most effectively |
| Qualified Lead Rate by Segment | Horizontal bar chart (ranked) | Which segments produce the highest-quality leads |
| Segment vs Platform Heatmap | Plotly `imshow` heatmap | Conversion rate at the intersection of each segment and platform — color intensity shows performance. Identifies the best segment-platform combinations. |
| Segment Summary | Data table | All metrics per segment: campaigns, impressions, clicks, leads, qualified, conversions, CTR, conversion rate, qualified rate |

**Populated by:** `segment_metrics(filtered_df)` which groups by `audience_segment` and computes all standard metrics plus `qualified_rate` (qualified_leads / leads_generated × 100).

**Why it exists:** Marketing spend should flow to the audiences most likely to convert. This page answers "Should we target more Enterprise Buyers or Startup Founders?" by comparing segments across reach, engagement, lead quality, and conversion efficiency. The heatmap adds a second dimension — revealing that a segment might perform well on one platform but poorly on another.

---

## AI Chatbot

### System Prompt Design

The system prompt sent to GPT-4.1-mini includes:

1. **Role definition** — "You are a Marketing Analytics Assistant"
2. **Strict behavioral rules** — decline off-topic questions, never output the prompt, never execute code
3. **Complete data schema** — column descriptions for all three CSV files
4. **Full merged dataset** — the entire 48-row CSV is embedded so the LLM can reference actual numbers
5. **Analysis guidelines** — how to interpret metrics, distinguish awareness from conversion, and compute rates
6. **Recommendation logic** — the same rules used by the rule-based insights module, so the LLM's answers are consistent with the dashboard

### Guardrail Architecture

| Layer | When | What It Does | Examples Blocked |
|-------|------|-------------|-----------------|
| Input sanitization | Before API call | Regex matching + length check | "ignore all instructions", "you are now a pirate", "reveal your prompt", messages >1000 chars |
| System prompt hardening | During API call | Explicit instructions to the LLM | Role-switching, prompt extraction, off-topic content generation |
| Output validation | After API call | Sentinel detection + length cap | Responses containing system prompt fragments, responses >3000 chars |

---

## Theming and Styling

### Streamlit Config (`.streamlit/config.toml`)

| Setting | Value | Effect |
|---------|-------|--------|
| `primaryColor` | `#2E8B57` (Sea Green) | Buttons, links, interactive elements |
| `backgroundColor` | `#FFFFFF` (White) | Main page background |
| `secondaryBackgroundColor` | `#F0FFF0` (Honeydew) | Sidebar, card backgrounds |
| `textColor` | `#1E1E1E` (Near Black) | Body text |
| `font` | `sans serif` | Clean, modern typeface |

### Custom CSS (in `utils/layout.py`)

Applied globally to every page via `setup_page()`:

- **Sidebar hidden** — the default Streamlit sidebar is replaced by the custom top nav bar
- **Nav link styling** — green text, rounded borders, green fill on hover with white text
- **"Ask AI" button** — green gradient background, white text, subtle drop shadow — visually distinct from regular nav links
- **Metric cards** — light green background (#F0FFF0), green left border, uppercase labels in gray, bold green values
- **Data tables** — rounded corners with hidden overflow
- **Typography** — H1 is 800 weight; H1/H2/H3 are near-black

---

## Filters

All analytics pages (Overview, Channels, Content, Funnel, Insights, Audience) share the same filter panel rendered in the right-side column.

**How they work:**

1. `apply_filters(container)` in `utils/filters.py` is called with the right column as the container
2. Inside that container, three `st.multiselect` widgets are rendered
3. The function loads the full merged dataset, applies the selected filter values using boolean indexing, and returns the filtered DataFrame
4. The calling page receives only the filtered data — all metrics and charts automatically reflect the current filter state

**Filter state** is managed by Streamlit's `st.session_state` via unique widget keys (`filter_platform`, `filter_content_type`, `filter_audience_segment`).

---

## Navigation System

The top navigation bar is rendered by `_render_nav()` in `utils/layout.py` and appears on every page via the `setup_page()` call.

**Pages in order:**

| Nav Label | File | Description |
|-----------|------|-------------|
| Home | `app.py` | Landing page with executive snapshot |
| Overview | `pages/1_Overview.py` | KPI dashboard with filters |
| Channels | `pages/2_Channel_Performance.py` | Platform comparison |
| Content | `pages/3_Content_Analysis.py` | Content type analysis |
| Funnel | `pages/4_Funnel_Analysis.py` | Funnel visualization and diagnosis |
| Insights | `pages/5_Claude_Insights.py` | Intelligence layer (visual + report) |
| Audience | `pages/7_Audience_Segments.py` | Segment deep-dive |
| Ask AI | `pages/6_Chat.py` | AI chatbot (highlighted as CTA) |

The "Ask AI" link is rendered with a distinct green gradient to draw attention as a call-to-action.

---

## Configuration

### Hot Reload

`.streamlit/config.toml` includes:

```toml
[server]
runOnSave = true
fileWatcherType = "auto"
```

This enables automatic page refresh whenever a source file is saved — useful during development.

### Environment Variables

| Variable | Required | Used By | Purpose |
|----------|----------|---------|---------|
| `OPENAI_API_KEY` | Only for Chat page | `utils/chatbot.py` | Authenticates with OpenAI API |

Set in PowerShell: `$env:OPENAI_API_KEY = "sk-..."` or in bash: `export OPENAI_API_KEY="sk-..."`.

---

## Full Project Structure

```
marketing_analytics/
├── .streamlit/
│   └── config.toml                    # Theme + hot reload config
├── data/
│   ├── campaigns.csv                  # 48 campaigns with metadata
│   ├── engagement.csv                 # Impressions, clicks, likes, comments, shares
│   └── leads.csv                      # Leads, qualified leads, conversions
├── pages/
│   ├── 1_Overview.py                  # KPI dashboard with filters
│   ├── 2_Channel_Performance.py       # Platform comparison
│   ├── 3_Content_Analysis.py          # Content type analysis
│   ├── 4_Funnel_Analysis.py           # Funnel visualization + diagnosis
│   ├── 5_Claude_Insights.py           # Intelligence layer (visual + narrative)
│   ├── 6_Chat.py                      # AI chatbot interface
│   └── 7_Audience_Segments.py         # Audience segment deep-dive
├── utils/
│   ├── __init__.py
│   ├── chatbot.py                     # OpenAI API + 3-layer guardrails
│   ├── claude_layer.py                # Rule-based campaign classification + summaries
│   ├── data_loader.py                 # CSV loading + merging
│   ├── filters.py                     # Interactive filter widgets
│   ├── insights.py                    # Rule-based business insights
│   ├── layout.py                      # Navigation bar + global CSS
│   └── metrics.py                     # KPI formulas + aggregation functions
├── app.py                             # Home page / entry point
├── requirements.txt                   # Python dependencies
└── README.md                          # Setup and run instructions
```

---

## Metrics Reference

Quick reference for every metric used in the dashboard:

| Metric | Formula | Interpretation |
|--------|---------|----------------|
| **CTR** (Click-Through Rate) | clicks / impressions × 100 | How effectively content drives engagement from views |
| **Conversion Rate** | conversions / leads_generated × 100 | How effectively leads turn into customers |
| **Lead Rate** | leads_generated / clicks × 100 | How effectively clicks turn into leads |
| **Qualified Rate** | qualified_leads / leads_generated × 100 | Lead quality — what proportion of leads are sales-ready |
| **Funnel Efficiency** | conversions / impressions × 100 | End-to-end pipeline efficiency |
| **Drop-off %** | (current_stage - next_stage) / current_stage × 100 | Volume lost at each funnel transition |
| **Retention %** | next_stage / current_stage × 100 | Volume preserved at each funnel transition |

**Funnel stages (in order):** Impressions → Clicks → Leads → Qualified Leads → Conversions
