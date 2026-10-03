import streamlit as st

PRIMARY = "#2563EB"
PRIMARY_DARK = "#1E3A8A"
BG = "#FAFAFA"
CARD_BG = "#FFFFFF"
BORDER = "#E2E8F0"
TEXT_DARK = "#0F172A"
TEXT_MUTED = "#475569"


def apply_theme(hide_auth_pages: bool = True):
    """Call this once at the top of every page, right after st.set_page_config."""
    hide_css = ""
    if hide_auth_pages:
        hide_css = """
        [data-testid="stSidebarNav"] li:has(a[href$="/"]),
        [data-testid="stSidebarNav"] li:has(a[href*="Login"]),
        [data-testid="stSidebarNav"] li:has(a[href*="Register"]),
        [data-testid="stSidebarNav"] li:has(a[href*="Reset_Password"]),
        [data-testid="stSidebarNav"] li:has(a[href*="Verify_Email"]),
        [data-testid="stSidebarNav"] li:has(a[href*="Onboarding"]) {
            display: none !important;
        }
        """

    st.markdown(f"""
        <style>
        body, .stApp {{ background-color: {BG} !important; }}

        h1, h2, h3 {{ color: {TEXT_DARK} !important; font-weight: 700 !important; }}
        p, span, label {{ color: {TEXT_MUTED}; }}

        div[data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: {CARD_BG} !important;
            border: 1px solid {BORDER} !important;
            border-radius: 12px !important;
            padding: 1.5rem !important;
        }}

        div.stButton > button[kind="primary"] {{
            background-color: {PRIMARY} !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            border: none !important;
            font-weight: 600 !important;
        }}

        div.stButton > button[kind="secondary"] {{
            border-radius: 8px !important;
        }}

        [data-testid="stSidebar"] {{
            background-color: {CARD_BG} !important;
            border-right: 1px solid {BORDER};
        }}

        {hide_css}
        </style>
    """, unsafe_allow_html=True)