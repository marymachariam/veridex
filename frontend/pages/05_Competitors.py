import streamlit as st
from config import settings, Colors, Icons
from utils import api_client
from utils.theme import apply_theme
from components.chatbot import render_chatbot

if "token" not in st.session_state:
    st.switch_page("pages/01_Login.py")

st.set_page_config(page_title="VERIDEX - Competitors", layout=settings.PAGE_LAYOUT)
apply_theme()
render_chatbot()

with st.sidebar:
    st.markdown(f"**Logged in as:** {st.session_state.get('username', 'User')}")
    st.divider()
    if st.button("Logout", width='stretch'):
        st.session_state.clear()
        st.switch_page("pages/01_Login.py")
header_col1, header_col2 = st.columns([4, 1])
with header_col1:
    st.markdown(f"# {Icons.COMPETITOR} Competitor Directory")
    st.markdown("Track and manage tracked SaaS competitors")
with header_col2:
    st.write("")
    if st.button("⚖️ Compare", width='stretch'):
        st.switch_page("pages/10_Compare.py")
st.divider()

with st.expander("➕ Add New Competitor", expanded=False):
    with st.form("add_competitor_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Competitor Name *", placeholder="e.g. Acme Corp")
            website = st.text_input("Website", placeholder="e.g. acme.com")
        with col2:
            category = st.selectbox("Category *", ["CRM", "Analytics", "Marketing", "Security", "Other"])
            founded_year = st.number_input("Founded Year", min_value=1900, max_value=2026, value=2020)
        
        submitted = st.form_submit_button("Save Competitor", type="primary")
        if submitted:
            if not name:
                st.error("Competitor Name is required.")
            else:
                try:
                    res = api_client.create_competitor({"name": name, "category": category, "website": website, "founded_year": founded_year})
                    st.success(f"Added {name} successfully!")
                    st.rerun()
                except Exception as e:
                    msg = str(e)
                    if "plan" in msg.lower() or "trial" in msg.lower() or "subscri" in msg.lower():
                        st.warning(f"🔒 {msg}")
                        st.page_link("pages/13_Billing.py", label="View Plans →")
                    else:
                        st.error(f"Failed to create competitor: {msg}")

try:
    competitors = api_client.get_all_competitors()
except Exception:
    competitors = []

if competitors and isinstance(competitors, list):
    st.markdown(f"### Tracked Companies ({len(competitors)})")
    if "compare_selection" not in st.session_state:
        st.session_state.compare_selection = set()

    cols = st.columns(3)
    for idx, comp in enumerate(competitors):
        with cols[idx % 3]:
            with st.container(border=True):
                st.subheader(comp.get("name", "Unknown"))
                st.caption(f"Category: {comp.get('category', 'N/A')}")
                st.write(f"🌐 [{comp.get('website', 'N/A')}](https://{comp.get('website', '')})")
                st.caption(f"Founded: {comp.get('founded_year', 'N/A')}")
                checked = st.checkbox(
                    "Select for comparison",
                    value=comp["id"] in st.session_state.compare_selection,
                    key=f"compare_check_{comp['id']}",
                )
                if checked:
                    st.session_state.compare_selection.add(comp["id"])
                else:
                    st.session_state.compare_selection.discard(comp["id"])
                if st.button("📇 Battlecard", key=f"battlecard_btn_{comp['id']}", width='stretch'):
                    st.session_state["battlecard_preselect_id"] = comp["id"]
                    st.switch_page("pages/11_Battlecard.py")

    selected_count = len(st.session_state.compare_selection)
    st.divider()
    if selected_count >= 2:
        if st.button(f"⚖️ Compare {selected_count} Selected", type="primary"):
            id_to_name = {c["id"]: c["name"] for c in competitors}
            st.session_state["compare_preselect"] = [id_to_name[i] for i in st.session_state.compare_selection]
            st.switch_page("pages/10_Compare.py")
    else:
        st.caption("Select at least 2 competitors above to compare them.")
else:
    st.info("No competitors added yet. Use the form above to start tracking.")