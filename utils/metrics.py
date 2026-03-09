import pandas as pd


def calculate_ctr(clicks, impressions):
    if impressions == 0:
        return 0.0
    return (clicks / impressions) * 100


def calculate_conversion_rate(conversions, leads_generated):
    if leads_generated == 0:
        return 0.0
    return (conversions / leads_generated) * 100


def calculate_lead_rate(leads_generated, clicks):
    if clicks == 0:
        return 0.0
    return (leads_generated / clicks) * 100


def summarize_kpis(df: pd.DataFrame) -> dict:
    total_campaigns = len(df)
    total_impressions = int(df["impressions"].sum())
    total_clicks = int(df["clicks"].sum())
    total_leads = int(df["leads_generated"].sum())
    total_qualified = int(df["qualified_leads"].sum())
    total_conversions = int(df["conversions"].sum())

    ctr = calculate_ctr(total_clicks, total_impressions)
    conversion_rate = calculate_conversion_rate(total_conversions, total_leads)
    lead_rate = calculate_lead_rate(total_leads, total_clicks)

    return {
        "total_campaigns": total_campaigns,
        "total_impressions": total_impressions,
        "total_clicks": total_clicks,
        "total_leads": total_leads,
        "total_qualified_leads": total_qualified,
        "total_conversions": total_conversions,
        "ctr": round(ctr, 2),
        "conversion_rate": round(conversion_rate, 2),
        "lead_rate": round(lead_rate, 2),
    }


def platform_metrics(df: pd.DataFrame) -> pd.DataFrame:
    agg = df.groupby("platform").agg(
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        likes=("likes", "sum"),
        comments=("comments", "sum"),
        shares=("shares", "sum"),
        leads_generated=("leads_generated", "sum"),
        qualified_leads=("qualified_leads", "sum"),
        conversions=("conversions", "sum"),
        campaigns=("campaign_id", "count"),
    ).reset_index()

    agg["ctr"] = agg.apply(lambda r: round(calculate_ctr(r["clicks"], r["impressions"]), 2), axis=1)
    agg["conversion_rate"] = agg.apply(
        lambda r: round(calculate_conversion_rate(r["conversions"], r["leads_generated"]), 2), axis=1
    )
    agg["lead_rate"] = agg.apply(
        lambda r: round(calculate_lead_rate(r["leads_generated"], r["clicks"]), 2), axis=1
    )
    return agg


def content_type_metrics(df: pd.DataFrame) -> pd.DataFrame:
    agg = df.groupby("content_type").agg(
        impressions=("impressions", "sum"),
        clicks=("clicks", "sum"),
        likes=("likes", "sum"),
        comments=("comments", "sum"),
        shares=("shares", "sum"),
        leads_generated=("leads_generated", "sum"),
        qualified_leads=("qualified_leads", "sum"),
        conversions=("conversions", "sum"),
        campaigns=("campaign_id", "count"),
    ).reset_index()

    agg["ctr"] = agg.apply(lambda r: round(calculate_ctr(r["clicks"], r["impressions"]), 2), axis=1)
    agg["conversion_rate"] = agg.apply(
        lambda r: round(calculate_conversion_rate(r["conversions"], r["leads_generated"]), 2), axis=1
    )
    agg["lead_rate"] = agg.apply(
        lambda r: round(calculate_lead_rate(r["leads_generated"], r["clicks"]), 2), axis=1
    )
    return agg


def funnel_metrics(df: pd.DataFrame) -> list[dict]:
    stages = [
        ("Impressions", int(df["impressions"].sum())),
        ("Clicks", int(df["clicks"].sum())),
        ("Leads", int(df["leads_generated"].sum())),
        ("Qualified Leads", int(df["qualified_leads"].sum())),
        ("Conversions", int(df["conversions"].sum())),
    ]
    return [{"stage": name, "value": val} for name, val in stages]
