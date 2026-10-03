"""
Sidebar component
Navigation, filters, and controls
"""

import streamlit as st
from config import settings, Colors, Icons
from utils import StateHelpers, APIErrorHelpers, api_client


def render_navigation_menu():
    """Render main navigation menu"""
    st.markdown("### Navigation")
    
    nav_items = [
        (" Dashboard", "01_Dashboard"),
        (" Competitors", "02_Competitors"),
        (" Pricing Analysis", "03_Pricing_Analysis"),
        ("💬 Sentiment Analysis", "04_Sentiment_Analysis"),
        (" Price History", "05_Price_History"),
    ]
    
    for icon_name, page_file in nav_items:
        if st.button(icon_name, use_container_width=True, key=f"nav_{page_file}"):
            st.switch_page(f"pages/{page_file}.py")


def render_filter_section(title: str, filters: dict, on_filter_change):
    """
    Render a filter section in sidebar
    
    Args:
        title: Section title
        filters: Dictionary of filter_name: options
        on_filter_change: Callback when filters change
    """
    st.markdown(f"### {title}")
    
    for filter_name, options in filters.items():
        selected = st.selectbox(
            filter_name,
            options=options,
            key=f"filter_{filter_name}"
        )
        
        if callable(on_filter_change):
            on_filter_change(filter_name, selected)


def render_quick_actions(actions: dict):
    """
    Render quick action buttons
    
    Args:
        actions: Dictionary of action_name: callback
    """
    st.markdown("### Quick Actions")
    
    for action_name, callback in actions.items():
        if st.button(action_name, use_container_width=True, type="primary"):
            callback()


def render_system_status():
    """Render system status indicator"""
    st.markdown("### System Status")
    
    # Check API connection
    try:
        api_client.health_check()
        status_color = Colors.ACCENT_TEAL
        status_text = "Connected"
        status_icon = "✓"
    except Exception as e:
        status_color = Colors.ACCENT_RED
        status_text = "Disconnected"
        status_icon = "✗"
    
    st.markdown(
        f"""
        <div style='
            background-color: {Colors.NEUTRAL_50};
            border: 1px solid {Colors.NEUTRAL_200};
            border-radius: 6px;
            padding: 1rem;
        '>
            <p style='margin: 0; font-size: 12px; color: {Colors.NEUTRAL_400};'>
                API Status
            </p>
            <p style='margin: 5px 0 0 0; color: {status_color}; font-weight: 500;'>
                {status_icon} {status_text}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_sidebar_footer():
    """Render sidebar footer with info"""
    st.markdown("---")
    
    st.markdown("### About")
    
    st.markdown(
        f"""
        <p style='
            font-size: 11px;
            color: {Colors.NEUTRAL_400};
            line-height: 1.6;
            margin: 0;
        '>
        <strong>VERIDEX</strong><br>
        v{settings.API_VERSION}<br>
        {settings.ENVIRONMENT.upper()}<br><br>
        Professional SaaS Market Research Intelligence Platform
        </p>
        """,
        unsafe_allow_html=True
    )
    
    # Help links
    st.markdown(
        f"""
        <div style='font-size: 11px; margin-top: 1rem;'>
        <a href='#' style='color: {Colors.ACCENT_BLUE}; text-decoration: none;'>Documentation</a> |
        <a href='#' style='color: {Colors.ACCENT_BLUE}; text-decoration: none;'>Support</a> |
        <a href='#' style='color: {Colors.ACCENT_BLUE}; text-decoration: none;'>API</a>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_full_sidebar():
    """Render complete sidebar"""
    with st.sidebar:
        # Branding
        st.markdown(
            f"""
            <h2 style='
                margin: 0 0 0.5rem 0;
                color: {Colors.PRIMARY_DARK};
                font-size: 1.25rem;
            '>
                {Icons.COMPETITOR} {settings.APP_NAME}
            </h2>
            """,
            unsafe_allow_html=True
        )
        
        st.divider()
        
        # Navigation
        render_navigation_menu()
        
        st.divider()
        
        # System Status
        render_system_status()
        
        st.divider()
        
        # Footer
        render_sidebar_footer()