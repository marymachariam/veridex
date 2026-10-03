import streamlit as st

class UIHelpers:
    @staticmethod
    def show_error(msg):
        st.error(msg)
    
    @staticmethod
    def show_success(msg):
        st.success(msg)
    
    @staticmethod
    def show_info(msg):
        st.info(msg)
    
    @staticmethod
    def divider():
        st.divider()
    
    @staticmethod
    def spacer(n=1):
        for _ in range(n):
            st.write("")

class StateHelpers:
    @staticmethod
    def init_state(key, default):
        if key not in st.session_state:
            st.session_state[key] = default
    
    @staticmethod
    def get_state(key, default=None):
        return st.session_state.get(key, default)
    
    @staticmethod
    def set_state(key, value):
        st.session_state[key] = value
    
    @staticmethod
    def reset_state():
        st.session_state.clear()

class DataHelpers:
    pass

class ValidationHelpers:
    pass

class APIErrorHelpers:
    @staticmethod
    def handle_api_error(e):
        return f"API Error: {str(e)}"

class MetricHelpers:
    @staticmethod
    def calculate_percentage(value, total):
        return (value / total * 100) if total > 0 else 0
