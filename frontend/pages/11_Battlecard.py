import requests
import streamlit as st

from config import settings, Icons
from utils.theme import apply_theme
from components.chatbot import render_chatbot


st.set_page_config(page_title=f"{settings.APP_NAME} - Battlecard", layout="wide")
apply_theme()
render_chatbot()


if "token" not in st.session_state:
    st.switch_page("pages/01_Login.py")

st.markdown(f"# {Icons.COMPETITOR} Sales Battlecard")
st.caption("A quick-reference sheet to use during a live sales call.")

headers = {"Authorization": f"Bearer {st.session_state.token}"}

try:
    resp = requests.get(
        f"{settings.API_BASE_URL}/api/v1/competitors", headers=headers, params={"limit": 500}, timeout=settings.API_TIMEOUT
    )
    competitors = resp.json() if resp.status_code == 200 else []
except requests.RequestException:
    competitors = []

if not competitors:
    st.info("You don't have any competitors yet. Add one via Research or the Competitors page first.")
    st.stop()

name_by_id = {c["id"]: c["name"] for c in competitors}
id_by_name = {c["name"]: c["id"] for c in competitors}

preselect_id = st.session_state.pop("battlecard_preselect_id", None)
preselect_name = name_by_id.get(preselect_id)

selected_name = st.selectbox(
    "Choose a competitor",
    options=[c["name"] for c in competitors],
    index=[c["name"] for c in competitors].index(preselect_name) if preselect_name else 0,
)
competitor_id = id_by_name[selected_name]

generate = st.button("Generate Battlecard", type="primary")

cache_key = f"battlecard_{competitor_id}"
if generate:
    with st.spinner(f"Generating battlecard for {selected_name}..."):
        try:
            resp = requests.get(
                f"{settings.API_BASE_URL}/api/v1/battlecard/{competitor_id}", headers=headers, timeout=60
            )
        except requests.RequestException:
            st.error("Could not reach the server.")
            resp = None

    if resp is not None:
        if resp.status_code == 200:
            st.session_state[cache_key] = resp.json()
        elif resp.status_code == 401:
            st.error("Your session expired. Please log in again.")
        else:
            try:
                detail = resp.json().get("detail", "Battlecard generation failed.")
            except Exception:
                detail = "Battlecard generation failed."
            st.error(detail)

card = st.session_state.get(cache_key)
if card:
    st.divider()
    st.markdown(f"## {card['competitor_name']}")
    st.write(card["one_liner"])

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Why We Win")
        for point in card["why_we_win"]:
            st.write(f"- {point}")
    with col2:
        st.markdown("### Watch Out For")
        for point in card["watch_out_for"]:
            st.write(f"- {point}")

    st.markdown("### Pricing Summary")
    st.write(card["pricing_summary"])

    st.markdown("### Objection Handling")
    for item in card["objection_handling"]:
        with st.container(border=True):
            st.markdown(f"**If they say:** {item['objection']}")
            st.markdown(f"**You say:** {item['response']}")

    st.caption(f"Generated {card['generated_at']}")