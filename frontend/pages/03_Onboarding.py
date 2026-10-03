import streamlit as st
import requests
from config import settings, Icons
from components.chatbot import render_chatbot


st.set_page_config(page_title="VERIDEX - Onboarding", layout="centered")
render_chatbot()

if "token" not in st.session_state:
    st.switch_page("pages/01_Login.py")

st.markdown(f"# {Icons.COMPETITOR} Welcome to VERIDEX")
st.markdown("Set up your workspace by tracking your first competitor.")
st.progress(50, text="Step 1 of 2: Add initial competitor data")
st.divider()

with st.form("onboarding_competitor"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Competitor Name *", placeholder="Salesforce")
    with col2:
        category = st.selectbox("Category *", options=["CRM", "Project Management", "Communication", "Productivity"])

    website = st.text_input("Website", placeholder="salesforce.com")
    founded_year = st.number_input("Founded Year", min_value=1900, max_value=2026, value=2015)

    submitted = st.form_submit_button("Save & Continue to Dashboard", type="primary", width='stretch')

    if submitted:
        if not name:
            st.error("Competitor name is required.")
        else:
            try:
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                response = requests.post(
                    f"{settings.API_BASE_URL}/api/v1/competitors",
                    json={
                        "name": name,
                        "category": category,
                        "website": website,
                        "founded_year": founded_year
                    },
                    headers=headers,
                    timeout=settings.API_TIMEOUT
                )
                if response.status_code in [200, 201]:
                    st.session_state.onboarding_complete = True
                    st.switch_page("pages/04_Dashboard.py")
                else:
                    try:
                        detail = response.json().get("detail", "Failed to save competitor.")
                    except Exception:
                        detail = "Failed to save competitor."
                    st.error(detail)
            except requests.RequestException:
                st.error("Could not reach the server. Please try again.")