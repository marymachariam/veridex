import requests
import streamlit as st

from config import settings, Icons
from components.chatbot import render_chatbot

st.set_page_config(page_title=f"{settings.APP_NAME} - Verify Email", layout="centered", initial_sidebar_state="collapsed")

render_chatbot()

st.markdown(f"# {Icons.COMPETITOR} Verify your email")

token = st.query_params.get("token")

if not token:
    st.error("Missing verification token. Use the link from your email.")
else:
    with st.spinner("Verifying..."):
        try:
            resp = requests.post(f"{settings.API_BASE_URL}/api/v1/auth/verify-email", json={"token": token}, timeout=15)
        except requests.RequestException:
            resp = None

    if resp is not None and resp.status_code == 200:
        st.session_state.token = resp.json()["access_token"]
        st.success("Email verified! Redirecting...")
        st.switch_page("pages/04_Dashboard.py")
    else:
        try:
            detail = resp.json().get("detail", "Verification failed.") if resp else "Could not reach the server."
        except Exception:
            detail = "Verification failed."
        st.error(detail)
        st.page_link("pages/01_Login.py", label="Back to Login")