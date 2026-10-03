"""
Notification components for user feedback
Success, error, warning, info messages
"""

import streamlit as st


def show_success(message: str, icon: str = "✓"):
    """Show success notification"""
    st.success(f"{icon} {message}")


def show_error(message: str, icon: str = "✗"):
    """Show error notification"""
    st.error(f"{icon} {message}")


def show_warning(message: str, icon: str = "⚠️"):
    """Show warning notification"""
    st.warning(f"{icon} {message}")


def show_info(message: str, icon: str = "ℹ️"):
    """Show info notification"""
    st.info(f"{icon} {message}")