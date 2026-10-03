import requests
import streamlit as st

from config import settings, Icons
from utils.theme import apply_theme
from components.chatbot import render_chatbot

st.set_page_config(page_title=f"{settings.APP_NAME} - Compare", layout="wide")
apply_theme()
render_chatbot()

if "token" not in st.session_state:
    st.switch_page("pages/01_Login.py")

st.markdown(f"# {Icons.COMPETITOR} Compare Competitors")
st.caption("Pick 2 to 4 competitors to see pricing, features, and SWOT side by side.")

headers = {"Authorization": f"Bearer {st.session_state.token}"}
try:
    resp = requests.get(f"{settings.API_BASE_URL}/api/v1/competitors", headers=headers, params={"limit": 500}, timeout=settings.API_TIMEOUT)
    competitors = resp.json() if resp.status_code == 200 else []
except requests.RequestException:
    competitors = []

if not competitors:
    st.info("You don't have any competitors yet. Add one via Research or the Competitors page first.")
    st.stop()

name_by_id = {c["id"]: c["name"] for c in competitors}
preselect = st.session_state.pop("compare_preselect", [])
selected_names = st.multiselect(
    "Choose competitors",
    options=[c["name"] for c in competitors],
    default=[n for n in preselect if n in {c["name"] for c in competitors}],
    max_selections=4,
)

if len(selected_names) < 2:
    st.info("Select at least 2 competitors to compare.")
    st.stop()

id_by_name = {c["name"]: c["id"] for c in competitors}
selected_ids = [id_by_name[n] for n in selected_names]

with st.spinner("Loading comparison..."):
    try:
        resp = requests.post(
            f"{settings.API_BASE_URL}/api/v1/comparison",
            json={"competitor_ids": selected_ids},
            headers=headers,
            timeout=settings.API_TIMEOUT,
        )
    except requests.RequestException:
        st.error("Could not reach the server.")
        st.stop()

if resp.status_code != 200:
    st.error("Failed to load comparison.")
    st.stop()

data = resp.json()["competitors"]

st.divider()

# ---- Overview row ----
cols = st.columns(len(data))
for col, entry in zip(cols, data):
    comp = entry["competitor"]
    insight = entry.get("insight") or {}
    with col:
        st.markdown(f"### {comp['name']}")
        if comp.get("category"):
            st.caption(comp["category"])
        if insight.get("tagline"):
            st.write(f"*{insight['tagline']}*")
        if insight.get("summary"):
            st.write(insight["summary"])

st.divider()

# ---- Pricing table ----
st.markdown("## Pricing")
all_tiers = set()
for entry in data:
    for tier in entry["pricing"]:
        all_tiers.add(tier["tier_name"])

if all_tiers:
    pricing_cols = st.columns(len(data))
    for col, entry in zip(pricing_cols, data):
        with col:
            st.markdown(f"**{entry['competitor']['name']}**")
            if entry["pricing"]:
                for tier in entry["pricing"]:
                    price = f"${tier['price_usd']:,.0f}/{tier['billing_period']}" if tier.get("price_usd") is not None else "Contact sales"
                    st.write(f"{tier['tier_name']}: {price}")
            else:
                st.caption("No pricing data")
else:
    st.caption("No pricing data for any selected competitor yet.")

st.divider()

# ---- Features ----
st.markdown("## Features")
feature_cols = st.columns(len(data))
for col, entry in zip(feature_cols, data):
    with col:
        st.markdown(f"**{entry['competitor']['name']}**")
        if entry["features"]:
            for feat in entry["features"]:
                st.write(f"- {feat['feature_name']}")
        else:
            st.caption("No feature data")

st.divider()

# ---- SWOT ----
st.markdown("## SWOT")
swot_cols = st.columns(len(data))
labels = [("strengths", "Strengths"), ("weaknesses", "Weaknesses"), ("opportunities", "Opportunities"), ("threats", "Threats")]
for col, entry in zip(swot_cols, data):
    insight = entry.get("insight") or {}
    with col:
        st.markdown(f"**{entry['competitor']['name']}**")
        for key, label in labels:
            items = (insight.get(key) or "").split("\n")
            items = [i.strip() for i in items if i.strip()]
            if items:
                st.markdown(f"_{label}_")
                for item in items:
                    st.write(f"- {item}")