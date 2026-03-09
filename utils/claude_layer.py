import pandas as pd
from utils.metrics import (
    platform_metrics,
    content_type_metrics,
    funnel_metrics,
    calculate_ctr,
    calculate_conversion_rate,
)


THEME_MAP = {
    "Thought Leadership": "Awareness",
    "Educational Post": "Awareness",
    "Product Highlight": "Consideration",
    "Event Promotion": "Conversion",
    "Case Study": "Conversion",
}

INTENT_MAP = {
    "Thought Leadership": "Brand Visibility",
    "Educational Post": "Education",
    "Product Highlight": "Product Interest",
    "Event Promotion": "Event Registration / Lead Generation",
    "Case Study": "Trust Building / Conversion",
}


def classify_campaign_theme(row: pd.Series) -> str:
    return THEME_MAP.get(row["content_type"], "General")


def classify_campaign_intent(row: pd.Series) -> str:
    return INTENT_MAP.get(row["content_type"], "General")


def classify_funnel_stage(row: pd.Series) -> str:
    ctr = calculate_ctr(row["clicks"], row["impressions"])
    conv_rate = calculate_conversion_rate(row["conversions"], row["leads_generated"])

    if conv_rate > 30:
        return "Bottom-of-Funnel (Conversion)"
    if ctr > 5:
        return "Mid-Funnel (Consideration)"
    return "Top-of-Funnel (Awareness)"


def summarize_platform_performance(df: pd.DataFrame) -> str:
    pm = platform_metrics(df)
    best_reach = pm.loc[pm["impressions"].idxmax()]
    best_conv = pm.loc[pm["conversion_rate"].idxmax()]
    best_leads = pm.loc[pm["leads_generated"].idxmax()]

    lines = [
        f"**{best_reach['platform']}** is the strongest awareness channel with "
        f"{best_reach['impressions']:,} total impressions across {int(best_reach['campaigns'])} campaigns.",
        "",
        f"**{best_conv['platform']}** has the highest conversion efficiency at "
        f"{best_conv['conversion_rate']}%, making it the most effective for bottom-funnel outcomes.",
        "",
        f"**{best_leads['platform']}** generates the most leads overall ({int(best_leads['leads_generated'])}), "
        f"indicating strong mid-funnel performance.",
    ]

    if best_reach["platform"] != best_conv["platform"]:
        lines.append("")
        lines.append(
            f"There is a clear split between reach ({best_reach['platform']}) and "
            f"conversion ({best_conv['platform']}). A multi-channel strategy that leverages "
            f"{best_reach['platform']} for awareness and {best_conv['platform']} for conversion "
            f"would be most effective."
        )

    return "\n".join(lines)


def summarize_content_performance(df: pd.DataFrame) -> str:
    ct = content_type_metrics(df)
    best_reach = ct.loc[ct["impressions"].idxmax()]
    best_conv = ct.loc[ct["conversion_rate"].idxmax()]
    best_qual = ct.loc[(ct["qualified_leads"] / ct["leads_generated"].replace(0, 1)).idxmax()]

    lines = [
        f"**{best_reach['content_type']}** content drives the most visibility with "
        f"{best_reach['impressions']:,} impressions.",
        "",
        f"**{best_conv['content_type']}** content has the highest conversion rate at "
        f"{best_conv['conversion_rate']}%, suggesting it resonates with decision-ready audiences.",
        "",
        f"**{best_qual['content_type']}** content produces the strongest qualified-lead ratio, "
        f"making it ideal for deeper funnel engagement.",
    ]

    return "\n".join(lines)


def identify_funnel_issue(df: pd.DataFrame) -> str:
    funnel = funnel_metrics(df)
    max_drop_pct = 0.0
    drop_from = ""
    drop_to = ""

    for i in range(len(funnel) - 1):
        current = funnel[i]["value"]
        next_val = funnel[i + 1]["value"]
        if current == 0:
            continue
        drop_pct = ((current - next_val) / current) * 100
        if drop_pct > max_drop_pct:
            max_drop_pct = drop_pct
            drop_from = funnel[i]["stage"]
            drop_to = funnel[i + 1]["stage"]

    issue_explanations = {
        ("Impressions", "Clicks"): (
            "The largest drop-off is from Impressions to Clicks. "
            "This typically indicates weak ad creative, poor targeting, or content that "
            "doesn't compel action. Consider A/B testing headlines and visuals."
        ),
        ("Clicks", "Leads"): (
            "The largest drop-off is from Clicks to Leads. "
            "Visitors are engaging but not converting to leads. This suggests "
            "landing page friction, weak CTAs, or misaligned expectations between "
            "the ad and the destination."
        ),
        ("Leads", "Qualified Leads"): (
            "The largest drop-off is from Leads to Qualified Leads. "
            "Many leads are entering the funnel but not qualifying. "
            "Consider tightening targeting criteria or using gated content "
            "that filters for higher-intent prospects."
        ),
        ("Qualified Leads", "Conversions"): (
            "The largest drop-off is from Qualified Leads to Conversions. "
            "Prospects are interested but not closing. This often points to "
            "sales process friction, pricing objections, or missing nurture sequences."
        ),
    }

    explanation = issue_explanations.get(
        (drop_from, drop_to),
        f"The largest drop-off occurs between {drop_from} and {drop_to} ({max_drop_pct:.1f}%)."
    )

    return f"{explanation}\n\n**Drop-off magnitude:** {max_drop_pct:.1f}%"


def generate_founder_recommendations(df: pd.DataFrame) -> str:
    pm = platform_metrics(df)
    ct = content_type_metrics(df)
    funnel = funnel_metrics(df)

    best_reach_platform = pm.loc[pm["impressions"].idxmax(), "platform"]
    best_conv_platform = pm.loc[pm["conversion_rate"].idxmax(), "platform"]
    best_conv_content = ct.loc[ct["conversion_rate"].idxmax(), "content_type"]
    best_reach_content = ct.loc[ct["impressions"].idxmax(), "content_type"]

    total_impressions = funnel[0]["value"]
    total_conversions = funnel[-1]["value"]
    overall_rate = (total_conversions / total_impressions * 100) if total_impressions else 0

    recs = []

    recs.append(
        f"**Double down on {best_conv_platform}** for conversion campaigns. "
        f"It delivers the highest ROI per lead."
    )

    recs.append(
        f"**Use {best_reach_platform} as the primary awareness channel.** "
        f"It consistently generates the highest reach and visibility."
    )

    recs.append(
        f"**Scale {best_conv_content} content** -- it has the strongest conversion rate "
        f"and should be a core part of bottom-funnel strategy."
    )

    recs.append(
        f"**Pair {best_reach_content} with stronger CTAs.** "
        f"High visibility content needs clearer paths to conversion."
    )

    recs.append(
        f"**Overall funnel efficiency is {overall_rate:.2f}%.** "
        f"Focus on reducing the largest drop-off point to improve end-to-end conversion."
    )

    return "\n\n".join(recs)
