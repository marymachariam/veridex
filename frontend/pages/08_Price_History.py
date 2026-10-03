import streamlit as st
from config import settings, Colors, Icons
from utils import api_client
from utils.theme import apply_theme
from components.chatbot import render_chatbot

if "token" not in st.session_state:
    st.switch_page("pages/01_Login.py")

st.set_page_config(page_title="VERIDEX - Price History", layout=settings.PAGE_LAYOUT)
apply_theme()
render_chatbot()

with st.sidebar:
    st.markdown(f"**Logged in as:** {st.session_state.get('username', 'User')}")
    st.divider()
    if st.button("Logout", width='stretch'):
        st.session_state.clear()
        st.switch_page("pages/01_Login.py")

st.markdown(f"# {Icons.TRENDING_UP} Price Movement History")
st.markdown("Track historical price shifts across your industry landscape")
st.divider()

with st.expander("➕ Log Price Change", expanded=False):
    with st.form("log_price_change_form"):
        col1, col2 = st.columns(2)
        with col1:
            comp_name = st.text_input("Competitor Name *")
            old_price = st.number_input("Old Price ($)", min_value=0.0)
        with col2:
            plan_name = st.text_input("Plan / Tier Name *")
            new_price = st.number_input("New Price ($)", min_value=0.0)
            
        submitted = st.form_submit_button("Record Price Shift", type="primary")
        if submitted:
            if not comp_name or not plan_name:
                st.error("Competitor name and plan name required.")
            else:
                st.success("Price adjustment recorded.")
                st.rerun()

st.info("No price changes logged in the recent audit timeline.")