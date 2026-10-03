import streamlit as st
import requests

from config import settings, Icons
from utils.theme import apply_theme
from utils.report_view import render_report
from components.chatbot import render_chatbot

st.set_page_config(page_title=f"{settings.APP_NAME} - Research", layout="wide")
apply_theme()
render_chatbot()

if "token" not in st.session_state:
    st.switch_page("pages/01_Login.py")

st.markdown(f"# {Icons.COMPETITOR} Competitor Research")
st.caption("Enter a competitor and VERIDEX will research pricing, positioning, features and SWOT automatically.")

with st.form("research_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Competitor name *", placeholder="e.g. Notion")
    with col2:
        website = st.text_input("Website (optional)", placeholder="notion.so")
    run = st.form_submit_button("Run Research", type="primary", width='stretch')

if run:
    if not name:
        st.error("Enter a competitor name.")
    else:
        with st.spinner(f"Researching {name} — this can take 20-40 seconds..."):
            try:
                headers = {"Authorization": f"Bearer {st.session_state.token}"}
                response = requests.post(
                    f"{settings.API_BASE_URL}/api/v1/research/competitor",
                    json={"name": name, "website": website or None},
                    headers=headers,
                    timeout=90,
                )
            except requests.RequestException:
                st.error("Could not reach the server.")
                response = None

        if response is not None:
            if response.status_code == 200:
                st.session_state["last_research"] = response.json()
                st.success(f"Research complete for {name}. Saved to your Research History.")
            elif response.status_code == 401:
                st.error("Your session expired. Please log in again.")
            else:
                try:
                    detail = response.json().get("detail", "Research failed.")
                except Exception:
                    detail = "Research failed."
                st.error(detail)

report = st.session_state.get("last_research")
if report:
    st.divider()
    render_report(report)

    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("View in Dashboard →", type="primary"):
            st.switch_page("pages/04_Dashboard.py")
    with col_b:
        if st.button("📚 Research History"):
            st.switch_page("pages/16_History.py")