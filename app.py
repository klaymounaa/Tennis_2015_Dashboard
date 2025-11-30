
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# -------------------------------------------
# CONFIG
# -------------------------------------------
st.set_page_config(page_title="Tennis Dashboard", layout="wide")

DATA_PATH = os.path.join(os.path.dirname(__file__),"atp_matches_2015_updated.csv")  

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

try:
    df = load_data(DATA_PATH)
except:
    st.error("❌ Cannot load the CSV file. Make sure it is in the same folder as app.py.")
    st.stop()

# -------------------------------------------
# COLOR THEME
# -------------------------------------------
WIN_COLOR = "Orange"
LOS_COLOR = "Crimson"
NEUTRAL = "Blue"
# -------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------
def tidy_vc(df, col, top=None):
    """Return tidy value_counts: col, count"""
    if col not in df.columns:
        return None
    vc = df[col].value_counts().reset_index()
    vc.columns = [col, "count"]
    if top:
        vc = vc.head(top)
    return vc

def numeric_summary(df, cols):
    """Return numeric summary table for given columns."""
    rows = []
    for c in cols:
        if c in df.columns and pd.api.types.is_numeric_dtype(df[c]):
            s = df[c].dropna()
            rows.append({
                "metric": c,
                "count": int(s.count()),
                "mean": round(float(s.mean()), 0),
                "median": round(float(s.median()), 1),
                "min": round(float(s.min()), 1),
                "max": round(float(s.max()), 1),
                "std": round(float(s.std()), 1)
            })
    return pd.DataFrame(rows).set_index("metric")

def metric_row(kpis, cols=4):
    c = st.columns(cols)
    for (label, value), col in zip(kpis.items(), c):
        col.metric(label, value)

# -------------------------------------------
# SIDEBAR
# -------------------------------------------
st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to:", [
    "Overview",
    "Tournament Details",
    "Winner Details",
    "Loser Details",
    "Match Details",
    "Winner Match Statistics",
    "Loser Match Statistics"
])

# -------------------------------------------
# KPIs
# -------------------------------------------
total_matches = len(df)
unique_tourneys = df["tourney_name"].nunique() if "tourney_name" in df else "-"
unique_winners = df["winner_name"].nunique() if "winner_name" in df else "-"
unique_losers = df["loser_name"].nunique() if "loser_name" in df else "-"
unique_players = len(pd.unique(df[["winner_name", "loser_name"]].values.ravel()))


# ======================================================================
# OVERVIEW
# ======================================================================
if section == "Overview":
    st.title("🎾 Tennis Data Overview (Totals)")

    metric_row({
        "Total Matches": f"{total_matches:,}",
        "Tournaments": f"{unique_tourneys:,}",
        "Winners": f"{unique_winners:,}",
        "Losers": f"{unique_losers:,}"
    })

    st.subheader("Dataset Sample")
    st.dataframe(df.head(10), use_container_width=True)

    st.subheader("Overall Numeric Summary")
    numeric_fields = [
        "minutes", "sets_num",
        "winner_age", "loser_age",
        "winner_ht", "loser_ht",
        "w_ace", "l_ace", "w_df", "l_df",
        "w_svpt", "l_svpt",
        "w_1stIn", "w_1stWon", "l_1stIn", "l_1stWon"
    ]
    numeric_cols = [c for c in numeric_fields if c in df.columns]

    if numeric_cols:
        st.dataframe(numeric_summary(df, numeric_cols))


# ======================================================================
# TOURNAMENT DETAILS
# ======================================================================
elif section == "Tournament Details":
    st.title("🏟 Tournament Details")

    # ------------------------------------------------------------
    # Matches per tournament (Top 30)
    # ------------------------------------------------------------
    vc_t = tidy_vc(df, "tourney_name", top=30)
    if vc_t is not None:
        st.subheader("Matches per Tournament (Top 30)")
        fig = px.bar(
            vc_t,
            x="tourney_name",
            y="count",
            title="Matches per Tournament",
            color_discrete_sequence=[NEUTRAL]
        )
        st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------
    # Surface distribution
    # ------------------------------------------------------------
    vc_surf = tidy_vc(df, "surface")
    if vc_surf is not None:
        st.subheader("Matches per Surface")
        fig = px.pie(
            vc_surf,
            names="surface",
            values="count",
            title="Matches by Surface",
            color_discrete_sequence=[NEUTRAL, WIN_COLOR, LOS_COLOR]
        )
        st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------
    # Monthly matches (CALENDAR ORDER — Using your structure)
    # ------------------------------------------------------------
    st.subheader("Matches per Month (Calendar Order)")

    if {"tourney_month_num", "tourney_month_name"}.issubset(df.columns):

        # EXACT STRUCTURE YOU REQUESTED:
        monthly = (
            df.groupby(["tourney_month_num", "tourney_month_name"])
              .size()
              .reset_index(name="count")
        )
        monthly = monthly.sort_values("tourney_month_num")

        fig = px.bar(
            monthly,
            x="tourney_month_name",
            y="count",
            title="Matches per Month (Ordered Jan → Dec)",
            color_discrete_sequence=[NEUTRAL]
        )
        st.plotly_chart(fig, use_container_width=True)

    else:
        # FALLBACK (alphabetical)
        vc_month = tidy_vc(df, "tourney_month_name")
        if vc_month is not None:
            fig = px.bar(
                vc_month,
                x="tourney_month_name",
                y="count",
                title="Matches per Month",
                color_discrete_sequence=[NEUTRAL]
            )
            st.plotly_chart(fig, use_container_width=True)

    # ------------------------------------------------------------
    # Draw Size Distribution — Curve + Bar (Correct Categories)
    # ------------------------------------------------------------
    if "draw_size" in df.columns:
        st.subheader("Draw Size Distribution (Correct Tournament Categories)")

        ds = df["draw_size"].value_counts().reset_index()
        ds.columns = ["draw_size", "count"]
        ds = ds.sort_values("draw_size")

        # Curve chart
        fig_curve = px.line(
            ds,
            x="draw_size",
            y="count",
            markers=True,
            title="Draw Size Curve (8, 16, 28, 32, 64, 128...)",
            color_discrete_sequence=[NEUTRAL]
        )
        fig_curve.update_layout(
            xaxis_title="Draw Size",
            yaxis_title="Number of Matches",
            showlegend=False
        )
        st.plotly_chart(fig_curve, use_container_width=True)

# ======================================================================
# WINNER DETAILS
# ======================================================================
elif section == "Winner Details":
    st.title("🏆 Winner Details")

    # Top winners
    wc = tidy_vc(df, "winner_name", top=20)
    if wc is not None:
        st.subheader("Top 20 Match Winners")
        fig = px.bar(
            wc, x="winner_name", y="count",
            color_discrete_sequence=[WIN_COLOR],
            title="Top 20 Winners"
        )
        st.plotly_chart(fig, use_container_width=True)

    # Winner country (IOC)
    w_ioc = tidy_vc(df, "winner_ioc")
    if w_ioc is not None:
        st.subheader("Winner Country Distribution (IOC Codes)")
        fig = px.bar(
            w_ioc.head(20),
            x="winner_ioc",
            y="count",
            title="Top 20 Winner Countries",
            color_discrete_sequence=[WIN_COLOR]
        )
        st.plotly_chart(fig, use_container_width=True)

    # Winner numeric summary
    w_nums = [c for c in ["winner_age", "winner_ht", "winner_rank"] if c in df]
    if w_nums:
        st.subheader("Winner Numeric Summary")
        st.dataframe(numeric_summary(df, w_nums))

    # Winner hand distribution
    wh = tidy_vc(df, "winner_hand")
    if wh is not None:
        st.subheader("Winner Hand Distribution")
        fig = px.pie(
            wh,
            names="winner_hand",
            values="count",
            title="Winner Hand",
            color_discrete_sequence=[WIN_COLOR, NEUTRAL]
        )
        st.plotly_chart(fig, use_container_width=True)

# ======================================================================
# LOSER DETAILS
# ======================================================================
elif section == "Loser Details":
    st.title("📉 Loser Details")

    # Top losers
    lc = tidy_vc(df, "loser_name", top=20)
    if lc is not None:
        st.subheader("Top 20 Match Losers")
        fig = px.bar(
            lc, x="loser_name", y="count",
            title="Top 20 Losers",
            color_discrete_sequence=[LOS_COLOR]
        )
        st.plotly_chart(fig, use_container_width=True)

    # Loser country (IOC)
    l_ioc = tidy_vc(df, "loser_ioc")
    if l_ioc is not None:
        st.subheader("Loser Country Distribution (IOC Codes)")
        fig = px.bar(
            l_ioc.head(20),
            x="loser_ioc",
            y="count",
            title="Top 20 Loser Countries",
            color_discrete_sequence=[LOS_COLOR]
        )
        st.plotly_chart(fig, use_container_width=True)

    # Loser numeric summary
    l_nums = [c for c in ["loser_age", "loser_ht", "loser_rank"] if c in df]
    if l_nums:
        st.subheader("Loser Numeric Summary")
        st.dataframe(numeric_summary(df, l_nums))

    # Loser hand distribution
    lh = tidy_vc(df, "loser_hand")
    if lh is not None:
        st.subheader("Loser Hand Distribution")
        fig = px.pie(
            lh,
            names="loser_hand",
            values="count",
            title="Loser Hand",
            color_discrete_sequence=[LOS_COLOR, NEUTRAL]
        )
        st.plotly_chart(fig, use_container_width=True)

# ======================================================================
# MATCH DETAILS
# ======================================================================
elif section == "Match Details":
    st.title("⏱ Match Details")

    if "minutes" in df.columns:
        st.subheader("Match Duration Distribution")
        fig = px.histogram(df, x="minutes", nbins=50,
                           color_discrete_sequence=[NEUTRAL])
        st.plotly_chart(fig, use_container_width=True)

        col = st.columns(2)
        col[0].metric("Average minutes", round(df["minutes"].mean(), 2))
        col[1].metric("Median minutes", round(df["minutes"].median(), 2))

    if "sets_num" in df.columns:
        st.subheader("Sets per Match")
        fig = px.histogram(df, x="sets_num", nbins=10,
                           color_discrete_sequence=[NEUTRAL])
        st.plotly_chart(fig, use_container_width=True)

    # FIXED SCORE TABLE
    if "score" in df.columns:
        st.subheader("Most Common Scores")
        score_df = df["score"].value_counts().reset_index()
        score_df.columns = ["score_value", "score_count"]
        st.dataframe(score_df.head(20))

    if "round" in df.columns:
        st.subheader("Round Distribution")
        rd = tidy_vc(df, "round")
        fig = px.bar(rd, x="round", y="count",
                     color_discrete_sequence=[NEUTRAL])
        st.plotly_chart(fig, use_container_width=True)


# ======================================================================
# WINNER MATCH STATISTICS
# ======================================================================
elif section == "Winner Match Statistics":
    st.title("📊 Winner Match Statistics")

    w_stats = [c for c in ["w_ace","w_df","w_svpt","w_1stIn","w_1stWon"] if c in df]
    if w_stats:
        st.subheader("Winner Stats Summary")
        st.dataframe(numeric_summary(df, w_stats))

    for c in w_stats:
        fig = px.histogram(df, x=c, nbins=40,
                           color_discrete_sequence=[WIN_COLOR],
                           title=f"{c} Distribution")
        st.plotly_chart(fig, use_container_width=True)


# ======================================================================
# LOSER MATCH STATISTICS
# ======================================================================
elif section == "Loser Match Statistics":
    st.title("📊 Loser Match Statistics")

    l_stats = [c for c in ["l_ace","l_df","l_svpt","l_1stIn","l_1stWon"] if c in df]
    if l_stats:
        st.subheader("Loser Stats Summary")
        st.dataframe(numeric_summary(df, l_stats))

    for c in l_stats:
        fig = px.histogram(df, x=c, nbins=40,
                           color_discrete_sequence=[LOS_COLOR],
                           title=f"{c} Distribution")
        st.plotly_chart(fig, use_container_width=True)
