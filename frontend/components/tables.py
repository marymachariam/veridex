"""
Table components for displaying data
Data tables, action rows
"""

import streamlit as st
import pandas as pd
from config import Colors


def render_data_table(data: list, columns: dict, key: str = ""):
    """
    Render a professional data table
    
    Args:
        data: List of dictionaries
        columns: Column configuration
        key: Unique key for the table
    """
    if not data:
        st.info("No data available")
        return
    
    df = pd.DataFrame(data)
    
    st.dataframe(
        df,
        column_config=columns,
        hide_index=True,
        use_container_width=True,
        key=key
    )


def render_action_row(label: str, actions: dict):
    """
    Render a row with action buttons
    
    Args:
        label: Row label
        actions: Dictionary of action_name: callback
    """
    cols = st.columns([3] + [1] * len(actions))
    
    with cols[0]:
        st.markdown(f"**{label}**")
    
    for idx, (action_name, action_callback) in enumerate(actions.items()):
        with cols[idx + 1]:
            if st.button(action_name, use_container_width=True, key=f"action_{label}_{action_name}"):
                action_callback()