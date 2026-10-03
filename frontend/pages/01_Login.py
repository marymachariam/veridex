import os
import streamlit as st
import requests
from config import settings, Colors, Icons
from components.chatbot import render_chatbot

st.set_page_config(
    page_title=f"{settings.APP_NAME} - Login",
    page_icon=settings.PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)


render_chatbot()

css_path = os.path.join(os.path.dirname(__file__), "..", "assets", "css", "main.css")
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.markdown("""
    <style>
    /* Hide Streamlit Sidebar Completely */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { 
        display: none !important; 
    }

    /* Page Container */
    .block-container {
        max-width: 1000px !important;
        padding-top: 4rem !important;
        padding-bottom: 4rem !important;
    }

    body, .stApp {
        background-color: #FAFAFA !important;
    }

    /* Left Hero / Pitch Column */
    .saas-hero {
        padding-right: 2rem;
        padding-top: 1rem;
    }

    .saas-hero h1 {
        font-size: 36px;
        font-weight: 800;
        color: #0F172A;
        line-height: 1.25;
        margin-top: 1rem;
    }

    .saas-hero p {
        font-size: 16px;
        color: #475569;
        margin-top: 1rem;
        line-height: 1.6;
    }

    /* Force Form Card Light Theme */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 16px !important;
        padding: 2.25rem !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01) !important;
    }

    /* CRITICAL FIX: Force Light Inputs Overriding Streamlit Dark Theme */
    div[data-testid="stTextInput"] div[data-baseweb="input"] {
        background-color: #F8FAFC !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }

    div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within {
        background-color: #FFFFFF !important;
        border-color: #2563EB !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15) !important;
    }

    div[data-testid="stTextInput"] input {
        color: #0F172A !important;
        -webkit-text-fill-color: #0F172A !important;
        background-color: transparent !important;
        font-size: 14px !important;
    }

    div[data-testid="stTextInput"] input::placeholder {
        color: #94A3B8 !important;
        -webkit-text-fill-color: #94A3B8 !important;
    }

    /* Label Styling */
    div[data-testid="stWidgetLabel"] label p {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    /* Primary Action Button */
    div.stButton > button[kind="primary"] {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border-radius: 8px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 0.65rem 1rem !important;
        font-size: 15px !important;
    }

    /* Google Sign-In Button */
    .google-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        width: 100%;
        padding: 0.6rem 1rem;
        border: 1px solid #CBD5E1;
        border-radius: 8px;
        background: #FFFFFF;
        color: #0F172A !important;
        font-weight: 600;
        font-size: 15px;
        text-decoration: none !important;
        margin-bottom: 1rem;
    }
    .google-btn:hover { background: #F8FAFC; border-color: #94A3B8; }
    .google-btn .g { font-weight: 800; color: #4285F4; font-size: 18px; }
    .or-divider {
        text-align: center;
        color: #94A3B8;
        font-size: 13px;
        margin: 0.75rem 0 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Handle return from Google sign-in
google_code = st.query_params.get("google_code")
if google_code and "token" not in st.session_state:
    try:
        r = requests.post(
            f"{settings.API_BASE_URL}/api/v1/auth/google/exchange",
            json={"code": google_code},
            timeout=settings.API_TIMEOUT,
        )
        if r.status_code == 200:
            access_token = r.json()["access_token"]
            st.session_state.token = access_token
            try:
                me = requests.get(
                    f"{settings.API_BASE_URL}/api/v1/auth/me",
                    headers={"Authorization": f"Bearer {access_token}"},
                    timeout=settings.API_TIMEOUT,
                )
                st.session_state.username = me.json().get("username", "") if me.ok else ""
            except requests.RequestException:
                st.session_state.username = ""
            st.query_params.clear()
            st.switch_page("pages/04_Dashboard.py")
        else:
            st.query_params.clear()
            st.error("Google sign-in expired. Please try again.")
    except requests.RequestException:
        st.error("Could not reach the server.")

# Authentication Session Check
if "token" in st.session_state:
    st.switch_page("pages/04_Dashboard.py")

# Show any error sent back from the Google flow
if st.query_params.get("google_error"):
    st.error(st.query_params.get("google_error"))

# Split Layout Columns
left_col, right_col = st.columns([1.1, 1], gap="large")

with left_col:
    st.markdown(f"""
        <div class="saas-hero">
            <div style="font-size: 42px; line-height: 1;">{Icons.COMPETITOR}</div>
            <h1>Welcome back to {settings.APP_NAME}</h1>
            <p>Access your real-time competitor analysis, pricing monitoring dashboards, and strategic market insights.</p>
        </div>
    """, unsafe_allow_html=True)

with right_col:
    with st.container(border=True):
        st.markdown("<h2 style='font-size: 22px; font-weight: 700; color: #0F172A; margin-bottom: 1.5rem;'>Log in</h2>", unsafe_allow_html=True)

        # Google sign-in button
        st.markdown(
            f'<a class="google-btn" href="{settings.API_BASE_URL}/api/v1/auth/google/login" target="_self">'
            '<span class="g">G</span> Continue with Google</a>'
            '<div class="or-divider">or log in with email</div>',
            unsafe_allow_html=True,
        )

        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Email or Username", placeholder="jane@company.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            
            st.write("")
            submitted = st.form_submit_button("Sign In", type="primary", width='stretch')

        with st.form("forgot_password_form"):
            st.caption("Forgot your password?")
            forgot_email = st.text_input("Enter your email", placeholder="jane@company.com", label_visibility="collapsed")
            forgot_submitted = st.form_submit_button("Send reset link")
            if forgot_submitted:
                if not forgot_email:
                    st.error("Enter your email.")
                else:
                    try:
                        requests.post(
                            f"{settings.API_BASE_URL}/api/v1/auth/forgot-password",
                            json={"email": forgot_email}, timeout=15,
                        )
                        st.success("If that email exists, a reset link has been sent.")
                    except requests.RequestException:
                        st.error("Could not reach the server.")

            if submitted:
                if not username or not password:
                    st.error("Please enter both email/username and password.")
                else:
                    try:
                        response = requests.post(
                            f"{settings.API_BASE_URL}/api/v1/auth/login",
                            json={"username": username, "password": password},
                            timeout=settings.API_TIMEOUT
                        )
                        if response.status_code == 200:
                            data = response.json()
                            st.session_state.token = data["access_token"]
                            st.session_state.username = username
                            st.switch_page("pages/04_Dashboard.py")
                        else:
                            try:
                                detail = response.json().get("detail", "Invalid email/username or password.")
                            except Exception:
                                detail = "Invalid email/username or password."
                            st.error(detail)
                    except Exception as e:
                        st.error(f"Connection error: {str(e)}")

    st.write("")
    footer_c1, footer_c2 = st.columns([1.8, 1])
    with footer_c1:
        st.markdown("<p style='margin-top: 8px; font-size: 14px; color: #475569; text-align: right;'>Don't have an account?</p>", unsafe_allow_html=True)
    with footer_c2:
        if st.button("Register here", width='stretch'):
            st.switch_page("pages/02_Register.py")