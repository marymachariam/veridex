"""
Navigation bar component
Top navigation with branding and user menu
"""

import streamlit as st
from config import settings, Colors, Icons
from utils import StateHelpers


def render_navbar():
    """
    Render professional top navigation bar
    """
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown(
            f"""
            <div style='display: flex; align-items: center; gap: 10px;'>
                <span style='font-size: 24px;'>{Icons.COMPETITOR}</span>
                <div>
                    <h3 style='margin: 0; color: {Colors.PRIMARY_DARK}; font-size: 18px;'>
                        {settings.APP_NAME}
                    </h3>
                    <p style='margin: 0; color: {Colors.NEUTRAL_400}; font-size: 11px;'>
                        Market Research Intelligence
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        # Search placeholder
        st.text_input(
            "Search",
            placeholder="Search competitors...",
            label_visibility="collapsed"
        )
    
    with col3:
        # User menu
        user_menu = st.selectbox(
            "Menu",
            ["Profile", "Settings", "Help", "Logout"],
            label_visibility="collapsed",
            key="user_menu"
        )
        
        if user_menu == "Logout":
            st.info("Logging out...")
            StateHelpers.reset_state()
            st.rerun()


def render_breadcrumb(items: list):
    """
    Render breadcrumb navigation
    
    Args:
        items: List of breadcrumb items
    """
    breadcrumb_html = " / ".join(
        f"<span style='color: {Colors.ACCENT_BLUE};'>{item}</span>"
        for item in items
    )
    
    st.markdown(
        f"<p style='font-size: 12px; color: {Colors.NEUTRAL_400}; margin: 0;'>{breadcrumb_html}</p>",
        unsafe_allow_html=True
    )