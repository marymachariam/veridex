"""
Card components for displaying data
Metric cards, stat cards, info cards
"""

import streamlit as st
from config import Colors, Typography


def render_metric_card(title: str, value: str, subtitle: str = "", icon: str = ""):
    """
    Render a metric card
    
    Args:
        title: Card title
        value: Main metric value
        subtitle: Additional subtitle text
        icon: Icon emoji
    """
    with st.container(border=True):
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{title}**")
            st.markdown(f"<h2 style='margin: 0; color: {Colors.PRIMARY_DARK};'>{value}</h2>", 
                       unsafe_allow_html=True)
            if subtitle:
                st.markdown(f"<p style='margin: 5px 0 0 0; color: {Colors.NEUTRAL_400}; font-size: 12px;'>{subtitle}</p>", 
                           unsafe_allow_html=True)
        
        with col2:
            if icon:
                st.markdown(f"<h1 style='text-align: center; margin: 0;'>{icon}</h1>", 
                           unsafe_allow_html=True)


def render_stat_card(label: str, value: str, change: str = "", change_positive: bool = True):
    """
    Render a statistic card with optional change indicator
    
    Args:
        label: Stat label
        value: Stat value
        change: Change amount (e.g., "+5.2%")
        change_positive: Whether change is positive (green) or negative (red)
    """
    with st.container(border=True):
        st.markdown(f"**{label}**")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"<h3 style='margin: 0; color: {Colors.PRIMARY_DARK};'>{value}</h3>", 
                       unsafe_allow_html=True)
        
        with col2:
            if change:
                change_color = Colors.ACCENT_TEAL if change_positive else Colors.ACCENT_RED
                st.markdown(f"<p style='margin: 0; color: {change_color}; text-align: right;'>{change}</p>", 
                           unsafe_allow_html=True)


def render_info_card(title: str, content: str, icon: str = "", icon_color: str = ""):
    """
    Render an information card
    
    Args:
        title: Card title
        content: Card content/description
        icon: Icon emoji
        icon_color: Color for the icon
    """
    with st.container(border=True):
        col1, col2 = st.columns([4, 1])
        
        with col1:
            st.markdown(f"**{title}**")
            st.markdown(f"<p style='margin: 0.5rem 0 0 0; font-size: 14px;'>{content}</p>", 
                       unsafe_allow_html=True)
        
        with col2:
            if icon:
                color_style = f"color: {icon_color};" if icon_color else ""
                st.markdown(f"<h2 style='text-align: center; margin: 0; {color_style}'>{icon}</h2>", 
                           unsafe_allow_html=True)