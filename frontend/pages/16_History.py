from datetime import datetime

import streamlit as st

from config import settings, Icons
from utils import api_client
from utils.report_view import render_report
from utils.theme import apply_theme
from components.chatbot import render_chatbot

st.set_page_config(page_title=f"{settings.APP_NAME} - Research History", layout="wide")
apply_theme()
render_chatbot()

if "token" not in st.session_state:
    st.switch_page("pages/01_Login.py")


def fmt_date(iso: str) -> str:
    try:
        return datetime.fromisoformat(iso).strftime("%d %b %Y, %H:%M UTC")
    except Exception:
        return iso or ""


st.markdown(f"# Research History")
st.caption("Every competitor research run, saved exactly as it was returned. Open any entry to see it again.")

search = st.text_input("Search", placeholder="Search by company name...", label_visibility="collapsed")
items = api_client.get_research_history(search=search or None, limit=100) or []

if not items:
    if search:
        st.info(f"No history matches '{search}'.")
    else:
        st.info("No research yet. Run your first competitor research and it will appear here.")
    if st.button("Go to Research", type="primary"):
        st.switch_page("pages/09_Research.py")
    st.stop()

list_col, view_col = st.columns([1, 2.2], gap="large")

with list_col:
    st.markdown(f"**{len(items)} saved run{'s' if len(items) != 1 else ''}**")
    for item in items:
        is_selected = st.session_state.get("history_selected_id") == item["id"]
        with st.container(border=True):
            st.markdown(f"**{'▶ ' if is_selected else ''}{item['competitor_name']}**")
            by = f" · {item['run_by']}" if item.get("run_by") else ""
            st.caption(f"{fmt_date(item['created_at'])}{by}")
            if st.button("Open", key=f"open_{item['id']}", width='stretch'):
                st.session_state["history_selected_id"] = item["id"]
                st.rerun()

with view_col:
    selected_id = st.session_state.get("history_selected_id")
    if not selected_id:
        st.info("Select an entry on the left to view the saved result.")
    else:
        detail = api_client.get_research_history_item(selected_id)
        if not detail:
            st.warning("This entry could not be loaded. It may have been deleted.")
            st.session_state.pop("history_selected_id", None)
        else:
            by = f" by {detail['run_by']}" if detail.get("run_by") else ""
            st.caption(f"Saved snapshot from {fmt_date(detail['created_at'])}{by}")
            render_report(detail["result"])

            st.divider()
            if st.button("Delete this entry", key="delete_history"):
                try:
                    api_client.delete_research_history_item(detail["id"])
                    st.session_state.pop("history_selected_id", None)
                    st.rerun()
                except Exception as e:
                    st.error(f"Could not delete: {e}")