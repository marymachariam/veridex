"""
Form components for data input
Text inputs, selects, sliders
"""

import streamlit as st
from config import Colors


def render_text_input(label: str, placeholder: str = "", value: str = "", required: bool = False):
    """
    Render a professional text input
    
    Args:
        label: Input label
        placeholder: Placeholder text
        value: Default value
        required: Is this field required
        
    Returns:
        Input value
    """
    required_mark = " *" if required else ""
    return st.text_input(
        f"{label}{required_mark}",
        value=value,
        placeholder=placeholder
    )


def render_select_input(label: str, options: list, value=None, required: bool = False):
    """
    Render a professional select input
    
    Args:
        label: Input label
        options: List of options
        value: Default value
        required: Is this field required
        
    Returns:
        Selected value
    """
    required_mark = " *" if required else ""
    return st.selectbox(
        f"{label}{required_mark}",
        options=options,
        index=0
    )


def render_slider_input(label: str, min_value: float, max_value: float, 
                       value: float = None, step: float = 1):
    """
    Render a professional slider input
    
    Args:
        label: Input label
        min_value: Minimum value
        max_value: Maximum value
        value: Default value
        step: Step size
        
    Returns:
        Selected value
    """
    if value is None:
        value = (min_value + max_value) / 2
    
    return st.slider(
        label,
        min_value=min_value,
        max_value=max_value,
        value=value,
        step=step
    )