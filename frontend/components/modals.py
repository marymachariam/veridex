"""
Modal/dialog components for confirmations and details
"""

import streamlit as st
from config import Colors


def render_confirmation_modal(title: str, message: str, on_confirm, on_cancel):
    """
    Render a confirmation modal
    
    Args:
        title: Modal title
        message: Confirmation message
        on_confirm: Callback when confirmed
        on_cancel: Callback when cancelled
    """
    st.warning(message)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Confirm", use_container_width=True, type="primary"):
            on_confirm()
    
    with col2:
        if st.button("Cancel", use_container_width=True):
            on_cancel()


def render_details_modal(title: str, details: dict):
    """
    Render a details modal
    
    Args:
        title: Modal title
        details: Dictionary of key-value pairs
    """
    st.markdown(f"### {title}")
    
    for key, value in details.items():
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown(f"**{key}:**")
        
        with col2:
            st.markdown(f"{value}")