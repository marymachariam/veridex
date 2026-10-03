import os
import html
import requests
import streamlit as st
from config import settings, Icons
from utils import api_client
from components.chatbot import render_chatbot

st.set_page_config(
    page_title=f"{settings.APP_NAME} - Register",
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
        max-width: 1100px !important;
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
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

    .feature-list {
        margin-top: 2rem;
    }

    .feature-item {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        font-size: 15px;
        color: #334155;
        margin-bottom: 1rem;
        font-weight: 500;
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
    div[data-testid="stTextInput"] div[data-baseweb="input"],
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background-color: #F8FAFC !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 8px !important;
    }

    div[data-testid="stTextInput"] div[data-baseweb="input"]:focus-within,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div:focus-within {
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

    .form-section-title {
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        margin-bottom: 0.75rem;
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

# ---------------------------------------------------------------------------
# "Check your email" screen, shown right after a successful registration
# ---------------------------------------------------------------------------
registered_email = st.session_state.get("registered_email")
if registered_email:
    _, center, _ = st.columns([1, 1.6, 1])
    with center:
        with st.container(border=True):
            safe_email = html.escape(registered_email)
            st.markdown(
                f"""
                <div style="text-align:center;">
                    <div style="font-size:64px; line-height:1;"></div>
                    <h2 style="font-size:24px; font-weight:800; color:#0F172A; margin:1rem 0 0.5rem 0;">Check your email</h2>
                    <p style="font-size:15px; color:#475569; line-height:1.6;">
                        We sent a verification link to<br><b style="color:#0F172A;">{safe_email}</b>
                    </p>
                    <p style="font-size:15px; color:#475569; line-height:1.6;">
                        Click the link to activate your account and start your <b>14-day free trial</b>.
                    </p>
                    <p style="font-size:13px; color:#94A3B8;">Can't find it? Check your spam folder.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.write("")
            if st.button("Go to Log in", type="primary", width="stretch"):
                st.session_state.pop("registered_email", None)
                st.switch_page("pages/01_Login.py")

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Resend email", width="stretch"):
                    try:
                        requests.post(
                            f"{settings.API_BASE_URL}/api/v1/auth/resend-verification",
                            json={"email": registered_email},
                            timeout=15,
                        )
                        st.success("A new link has been sent.")
                    except requests.RequestException:
                        st.error("Could not reach the server.")
            with c2:
                if st.button("Use a different email", width="stretch"):
                    st.session_state.pop("registered_email", None)
                    st.rerun()
    st.stop()

# ---------------------------------------------------------------------------
# Registration form
# ---------------------------------------------------------------------------
left_col, right_col = st.columns([1.1, 1], gap="large")

with left_col:
    st.markdown(f"""
        <div class="saas-hero">
            <div style="font-size: 42px; line-height: 1;">{Icons.COMPETITOR}</div>
            <h1>{settings.APP_NAME}</h1>
            <p>Empower your business decisions with automated market intelligence, competitor price tracking, and real-time sentiment analytics.</p>
            
            <div class="feature-list">
                <div class="feature-item">⚡ <b>Real-time Tracking</b> — Monitor competitor updates instantly.</div>
                <div class="feature-item"> <b>Deep Analytics</b> — Uncover market positioning trends.</div>
                <div class="feature-item"> <b>Enterprise Security</b> — SOC2 compliant intelligence workflow.</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with right_col:
    with st.container(border=True):
        st.markdown("<h2 style='font-size: 22px; font-weight: 700; color: #0F172A; margin-bottom: 1.5rem;'>Create your account</h2>", unsafe_allow_html=True)

        st.markdown(
            f'<a class="google-btn" href="{settings.API_BASE_URL}/api/v1/auth/google/login" target="_self">'
            '<span class="g">G</span> Sign up with Google</a>'
            '<div class="or-divider">or sign up with email</div>',
            unsafe_allow_html=True,
        )

        st.markdown("<div class='form-section-title'>User Details</div>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *", placeholder="Jane")
        with col2:
            last_name = st.text_input("Last Name *", placeholder="Smith")
            
        email = st.text_input("Work Email *", placeholder="jane@company.com")
        username = st.text_input("Username *", placeholder="janesmith")
        password = st.text_input("Password *", type="password", placeholder="••••••••")
        
        st.divider()
        st.markdown("<div class='form-section-title'>Company Information</div>", unsafe_allow_html=True)
        
        company_name = st.text_input("Company Name *", placeholder="Acme Corp")
        industry = st.selectbox(
            "Industry *",
            ["Technology", "E-commerce", "Healthcare", "Finance", "Education", "Other"]
        )
        
        st.write("")
        
        if st.button("Create Account", type="primary", width='stretch'):
            if not first_name or not last_name or not email or not username or not password or not company_name:
                st.error("Please fill in all required fields.")
            else:
                payload = {
                    "username": username,
                    "email": email,
                    "password": password,
                    "first_name": first_name,
                    "last_name": last_name,
                    "company_name": company_name,
                    "industry": industry
                }
                try:
                    response = api_client.register_user(payload)
                    if response:
                        st.session_state["registered_email"] = email.strip().lower()
                        st.rerun()
                    else:
                        st.error("Failed to create account. Username or email may already be taken.")
                except Exception as e:
                    st.error(f"Registration error: {str(e)}")

    st.write("")
    footer_c1, footer_c2 = st.columns([1.8, 1])
    with footer_c1:
        st.markdown("<p style='margin-top: 8px; font-size: 14px; color: #475569; text-align: right;'>Already have an account?</p>", unsafe_allow_html=True)
    with footer_c2:
        if st.button("Log In", width='stretch'):
            st.switch_page("pages/01_Login.py")