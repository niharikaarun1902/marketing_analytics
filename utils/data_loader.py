import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def load_campaigns() -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / "campaigns.csv")
    df["publish_date"] = pd.to_datetime(df["publish_date"], format="%d-%m-%Y")
    return df


def load_engagement() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "engagement.csv")


def load_leads() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "leads.csv")


def load_merged_data() -> pd.DataFrame:
    campaigns = load_campaigns()
    engagement = load_engagement()
    leads = load_leads()

    df = campaigns.merge(engagement, on="campaign_id", how="left")
    df = df.merge(leads, on="campaign_id", how="left")
    return df
