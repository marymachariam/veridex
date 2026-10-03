import streamlit as st
from config import settings, Colors, Icons
from utils import api_client
from utils.theme import apply_theme
from components.chatbot import render_chatbot

if "token" not in st.session_state:
    st.switch_page("pages/01_Login.py")

st.set_page_config(page_title="VERIDEX - Pricing Analysis", layout=settings.PAGE_LAYOUT)
apply_theme()
render_chatbot()

with st.sidebar:
    st.markdown(f"**Logged in as:** {st.session_state.get('username', 'User')}")
    st.divider()
    if st.button("Logout", width='stretch'):
        st.session_state.clear()
        st.switch_page("pages/01_Login.py")

st.markdown(f"# {Icons.PRICING} Pricing Tier Benchmarking")
st.markdown("Analyze competitor packaging and tier strategies")
st.divider()

with st.expander("➕ Log Pricing Tier", expanded=False):
    with st.form("add_pricing_form"):
        col1, col2 = st.columns(2)
        with col1:
            competitor_id = st.text_input("Competitor ID or Name *")
            plan_name = st.text_input("Plan Name *", placeholder="Pro / Enterprise")
        with col2:
            price = st.number_input("Monthly Price ($) *", min_value=0.0, value=29.99)
            billing_cycle = st.selectbox("Billing Cycle", ["Monthly", "Annual", "One-Time"])
        
        submitted = st.form_submit_button("Save Tier", type="primary")
        if submitted:
            if not competitor_id or not plan_name:
                st.error("Please fill in required fields.")
            else:
                st.success("Pricing tier recorded successfully.")
                st.rerun()

try:
    pricing = api_client.get_all_pricing()
except Exception:
    pricing = []

if pricing and isinstance(pricing, list):
    st.dataframe(pricing, width='stretch')
else:
    st.info("No pricing tier data available yet. Click 'Log Pricing Tier' to record data.")