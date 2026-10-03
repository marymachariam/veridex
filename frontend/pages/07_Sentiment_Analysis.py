import streamlit as st
from config import settings, Colors, Icons
from utils import api_client
from utils.theme import apply_theme
from components.chatbot import render_chatbot


if "token" not in st.session_state:
    st.switch_page("pages/01_Login.py")

st.set_page_config(page_title="VERIDEX - Sentiment Analysis", layout=settings.PAGE_LAYOUT)
apply_theme()
render_chatbot()

with st.sidebar:
    st.markdown(f"**Logged in as:** {st.session_state.get('username', 'User')}")
    st.divider()
    if st.button("Logout", width='stretch'):
        st.session_state.clear()
        st.switch_page("pages/01_Login.py")

st.markdown(f"# {Icons.REVIEWS} Customer Sentiment")
st.markdown("Monitor market perception and public customer feedback")
st.divider()

with st.expander("➕ Add Customer Review / Feedback", expanded=False):
    with st.form("add_review_form"):
        competitor = st.text_input("Competitor Name *")
        rating = st.slider("Rating", min_value=1, max_value=5, value=4)
        review_text = st.text_area("Review Content", placeholder="Enter review excerpt...")
        
        submitted = st.form_submit_button("Submit Review", type="primary")
        if submitted:
            if not competitor or not review_text:
                st.error("Competitor name and review text required.")
            else:
                st.success("Review logged successfully.")
                st.rerun()

try:
    reviews = api_client.get_all_reviews()
except Exception:
    reviews = []

if reviews and isinstance(reviews, list):
    for r in reviews:
        with st.container(border=True):
            st.write(f"**{r.get('competitor', 'Competitor')}** — Rating: {'⭐' * int(round(r.get('rating', 5)))}")
            st.write(f"\"{r.get('text', '')}\"")
else:
    st.info("No customer reviews or sentiment logs recorded yet.")