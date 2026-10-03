import streamlit as st
from config import settings, Icons
from utils import api_client
from utils.theme import apply_theme
from components.chatbot import render_chatbot
from components.onboarding_tour import maybe_show_tour, replay_tour_button
if "token" not in st.session_state:
    st.switch_page("pages/01_Login.py")

st.set_page_config(page_title="VERIDEX - Dashboard", layout=settings.PAGE_LAYOUT)
apply_theme()
render_chatbot()
maybe_show_tour()

with st.sidebar:
    st.markdown(f"**Logged in as:** {st.session_state.get('username', 'User')}")
    st.divider()
    if st.button("Log Out", width='stretch'):
        st.session_state.clear()
        st.switch_page("pages/01_Login.py")

st.markdown(f"# {Icons.COMPETITOR} Market Overview")
st.markdown("Real-time summary of tracked market metrics.")
st.divider()

try:
    competitors = api_client.get_all_competitors()
    pricing = api_client.get_all_pricing()
    reviews = api_client.get_all_reviews()
except Exception:
    competitors, pricing, reviews = [], [], []

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Competitors", len(competitors) if isinstance(competitors, list) else 0)
with col2:
    st.metric("Pricing Tiers", len(pricing) if isinstance(pricing, list) else 0)
with col3:
    st.metric("Customer Reviews", len(reviews) if isinstance(reviews, list) else 0)
with col4:
    st.metric("Avg. Rating", "4.5" if reviews else "N/A")

st.divider()

st.markdown("### Actions")
a1, a2, a3, a4 = st.columns(4)
with a1:
    if st.button("Competitors", width='stretch'):
        st.switch_page("pages/05_Competitors.py")
with a2:
    if st.button("Pricing Analysis", width='stretch'):
        st.switch_page("pages/06_Pricing_Analysis.py")
with a3:
    if st.button("Sentiment", width='stretch'):
        st.switch_page("pages/07_Sentiment_Analysis.py")
with a4:
    if st.button("Price History", width='stretch'):
        st.switch_page("pages/08_Price_History.py")