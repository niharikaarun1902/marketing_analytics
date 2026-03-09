import pandas as pd
from utils.metrics import (
    calculate_ctr,
    calculate_conversion_rate,
    calculate_lead_rate,
    platform_metrics,
    content_type_metrics,
    funnel_metrics,
)


def get_best_platform(df: pd.DataFrame) -> dict:
    pm = platform_metrics(df)
    return {
        "best_reach": pm.loc[pm["impressions"].idxmax(), "platform"],
        "best_clicks": pm.loc[pm["clicks"].idxmax(), "platform"],
        "best_leads": pm.loc[pm["leads_generated"].idxmax(), "platform"],
        "best_conversion_rate": pm.loc[pm["conversion_rate"].idxmax(), "platform"],
    }


def get_best_content_type(df: pd.DataFrame) -> dict:
    ct = content_type_metrics(df)
    return {
        "best_reach": ct.loc[ct["impressions"].idxmax(), "content_type"],
        "best_clicks": ct.loc[ct["clicks"].idxmax(), "content_type"],
        "best_leads": ct.loc[ct["leads_generated"].idxmax(), "content_type"],
        "best_conversion_rate": ct.loc[ct["conversion_rate"].idxmax(), "content_type"],
    }


def get_top_campaign(df: pd.DataFrame) -> pd.Series:
    return df.loc[df["conversions"].idxmax()]


def get_biggest_dropoff(df: pd.DataFrame) -> dict:
    funnel = funnel_metrics(df)
    max_drop_pct = 0.0
    drop_from = ""
    drop_to = ""
    drop_value = 0

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
            drop_value = current - next_val

    return {
        "from_stage": drop_from,
        "to_stage": drop_to,
        "drop_pct": round(max_drop_pct, 2),
        "drop_absolute": drop_value,
    }


def get_recommendations(df: pd.DataFrame) -> list[str]:
    recommendations = []
    pm = platform_metrics(df)
    ct = content_type_metrics(df)
    dropoff = get_biggest_dropoff(df)

    for _, row in pm.iterrows():
        if row["impressions"] > pm["impressions"].median() and row["ctr"] < pm["ctr"].median():
            recommendations.append(
                f"{row['platform']} has strong reach but below-average CTR. "
                f"Consider improving ad creative or messaging."
            )
        if row["clicks"] > pm["clicks"].median() and row["lead_rate"] < pm["lead_rate"].median():
            recommendations.append(
                f"{row['platform']} drives clicks but converts fewer leads. "
                f"Review CTAs and landing page alignment."
            )
        if row["conversion_rate"] > pm["conversion_rate"].median():
            recommendations.append(
                f"{row['platform']} shows strong conversion efficiency "
                f"({row['conversion_rate']}%). Consider scaling budget here."
            )

    for _, row in ct.iterrows():
        if row["qualified_leads"] / max(row["leads_generated"], 1) > 0.55:
            recommendations.append(
                f"{row['content_type']} content produces a strong qualified-lead rate. "
                f"Use it deeper in the funnel."
            )
        if row["impressions"] > ct["impressions"].median() and row["leads_generated"] < ct["leads_generated"].median():
            recommendations.append(
                f"{row['content_type']} generates awareness but fewer leads. "
                f"Pair with stronger CTAs or gated assets."
            )

    if dropoff["drop_pct"] > 80:
        recommendations.append(
            f"The largest funnel drop-off occurs between {dropoff['from_stage']} and "
            f"{dropoff['to_stage']} ({dropoff['drop_pct']}%). "
            f"This suggests a significant gap in engagement-to-action conversion."
        )

    return recommendations
