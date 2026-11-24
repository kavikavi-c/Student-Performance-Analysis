import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="VELoop Analytics", page_icon="🎮")
st.title("🎮 VELoop Analytics (Demo)")
st.caption("Engagement, XP, games, rewards, wallet and retention analysis.")

REQUIRED = ["user_id", "signup_week", "sessions", "games_played", "xp",
            "win_rate", "rewards_earned", "wallet_credit", "wallet_debit",
            "days_since_active"]

@st.cache_data
def make_sample(n=200):
    rng = np.random.default_rng(42)
    credit = rng.integers(0, 2000, n)
    return pd.DataFrame({
        "user_id": [f"U{i:03d}" for i in range(1, n + 1)],
        "signup_week": rng.integers(1, 9, n),
        "sessions": rng.integers(1, 60, n),
        "games_played": rng.integers(0, 120, n),
        "xp": rng.integers(0, 5000, n),
        "win_rate": np.clip(rng.normal(50, 15, n), 5, 95).round(1),
        "rewards_earned": rng.integers(0, 40, n),
        "wallet_credit": credit,
        "wallet_debit": np.minimum(rng.integers(0, 1500, n), credit),
        "days_since_active": rng.integers(0, 30, n),
    })

sample = make_sample()
st.download_button("⬇️ Sample VELoop CSV", sample.to_csv(index=False),
                   file_name="veloop_sample.csv", mime="text/csv")
up = st.file_uploader("Upload VELoop CSV (optional)", type="csv")

if up is not None:
    try:
        df = pd.read_csv(up)
    except Exception:
        st.error("Could not read the file. Please upload a valid CSV.")
        st.stop()
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        st.error("Missing columns: " + ", ".join(missing))
        st.stop()
    df = df[REQUIRED].copy()
    df["user_id"] = df["user_id"].astype(str)
    num = [c for c in REQUIRED if c != "user_id"]
    df[num] = df[num].apply(pd.to_numeric, errors="coerce")
    df = df.dropna().drop_duplicates(subset="user_id")
    if df.empty:
        st.error("No valid rows found after cleaning.")
        st.stop()
else:
    df = sample.copy()
    st.info("Showing simulated sample data (not real VELoop data).")

df["level"] = (df["xp"] // 500 + 1).astype(int)
df["wallet_balance"] = df["wallet_credit"] - df["wallet_debit"]
df["active"] = df["days_since_active"] <= 7

t1, t2, t3, t4, t5 = st.tabs(
    ["👥 Engagement", "⭐ XP", "🎲 Games", "💰 Rewards & Wallet", "🔁 Retention"]
)

with t1:
    a, b = st.columns(2)
    a.metric("Total Users", len(df))
    b.metric("Active (last 7 days)", int(df["active"].sum()))
    st.metric("Avg Sessions per User", round(df["sessions"].mean(), 1))
    st.subheader("Sessions Distribution")
    bins = [0, 10, 20, 30, 40, 50, 1000]
    labels = ["1-10", "11-20", "21-30", "31-40", "41-50", "50+"]
    st.bar_chart(pd.cut(df["sessions"], bins=bins, labels=labels)
                 .value_counts(sort=False), color="#2E7D32")

with t2:
    a, b = st.columns(2)
    a.metric("Average XP", round(df["xp"].mean()))
    b.metric("Highest Level", int(df["level"].max()))
    st.subheader("Users per Level (XP progression)")
    st.bar_chart(df["level"].value_counts().sort_index(), color="#EF6C00")
    st.subheader("Top 10 Users by XP")
    st.dataframe(df.nlargest(10, "xp")[["user_id", "xp", "level"]],
                 hide_index=True)

with t3:
    a, b = st.columns(2)
    a.metric("Avg Games Played", round(df["games_played"].mean(), 1))
    b.metric("Avg Win Rate", f"{df['win_rate'].mean():.1f}%")
    st.subheader("Games Played vs Win Rate")
    st.scatter_chart(df, x="games_played", y="win_rate")

with t4:
    a, b = st.columns(2)
    a.metric("Total Rewards", int(df["rewards_earned"].sum()))
    b.metric("Avg Wallet Balance", round(df["wallet_balance"].mean()))
    st.subheader("Wallet Credit vs Debit")
    st.bar_chart(pd.Series({"Credit": df["wallet_credit"].sum(),
                            "Debit": df["wallet_debit"].sum()}),
                 color="#1565C0")
    st.subheader("Average Rewards by Level")
    st.bar_chart(df.groupby("level")["rewards_earned"].mean(),
                 color="#6A1B9A")

with t5:
    st.subheader("Active Users % by Signup Week")
    ret = df.groupby("signup_week")["active"].mean().mul(100).round(1)
    st.line_chart(ret)
    st.subheader("Churn Risk (inactive more than 14 days)")
    risk = df[df["days_since_active"] > 14]
    st.warning(f"{len(risk)} user(s) at risk of leaving.")
    st.dataframe(risk[["user_id", "days_since_active", "sessions", "xp"]]
                 .sort_values("days_since_active", ascending=False),
                 hide_index=True)
