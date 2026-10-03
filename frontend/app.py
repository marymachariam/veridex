import os
import streamlit as st
from config import settings, Icons
from components.chatbot import render_chatbot

st.set_page_config(
    page_title=f"{settings.APP_NAME} - SaaS Market Intelligence",
    page_icon=settings.PAGE_ICON,
    layout="centered",
    initial_sidebar_state="collapsed"
)

render_chatbot()

# 1. Load Local CSS Tokens (assets/css/main.css)
css_path = os.path.join(os.path.dirname(__file__), "assets", "css", "main.css")
if os.path.exists(css_path):
    with open(css_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# 2. Add Layout & Component Overrides for Streamlit
st.markdown("""
    <style>
    /* Hide navigation sidebar for unauthenticated landing view */
    [data-testid="stSidebar"], [data-testid="collapsedControl"] { 
        display: none !important; 
    }

    /* Standardize Container Max Width (Fixes horizontal stretching) */
    .block-container {
        max-width: 960px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
    }

    /* Card Containers leveraging CSS Design Tokens */
    .feature-card {
        background-color: var(--neutral-100);
        border: 1px solid var(--neutral-200);
        border-radius: var(--radius-lg);
        padding: var(--space-lg);
        box-shadow: var(--shadow-sm);
        height: 100%;
    }

    .hero-title {
        font-size: var(--font-size-4xl);
        font-weight: var(--font-weight-bold);
        color: var(--primary-dark);
        text-align: center;
        line-height: 1.25;
        margin-bottom: var(--space-sm);
    }

    .hero-subtitle {
        font-size: var(--font-size-lg);
        color: var(--neutral-500);
        text-align: center;
        max-width: 680px;
        margin: 0 auto var(--space-xl) auto;
    }

    .stat-number {
        font-size: var(--font-size-3xl);
        font-weight: var(--font-weight-bold);
        color: var(--accent-blue);
        margin-bottom: 0px;
    }

    .stat-label {
        font-size: var(--font-size-sm);
        color: var(--neutral-500);
    }
    </style>
""", unsafe_allow_html=True)

# Redirect authenticated users straight to Dashboard
if "token" in st.session_state:
    st.switch_page("pages/04_Dashboard.py")

# --- NAVBAR ---
nav_left, nav_right = st.columns([3, 1])

with nav_left:
    st.markdown(f"### {Icons.COMPETITOR} **{settings.APP_NAME}**")

with nav_right:
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Log In", width='stretch'):
            st.switch_page("pages/01_Login.py")
    with c2:
        if st.button("Register", type="primary", width='stretch'):
            st.switch_page("pages/02_Register.py")

st.divider()

# --- HERO SECTION ---
st.markdown("<h1 class='hero-title'>Real-Time Market Research & Competitor Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Track pricing adjustments, sentiment trends, and market moves automatically with high-precision tracking.</p>", unsafe_allow_html=True)

_, cta_col, _ = st.columns([1, 1.2, 1])
with cta_col:
    if st.button("Start Free 14-Day Trial", type="primary", width='stretch'):
        st.switch_page("pages/02_Register.py")

st.write("")

# --- FEATURE PROOFS ---
st.divider()
s1, s2, s3, s4 = st.columns(4)
with s1:
    st.markdown("<div style='text-align: center;'><p class='stat-number'>AI</p><p class='stat-label'>Automated Research</p></div>", unsafe_allow_html=True)
with s2:
    st.markdown("<div style='text-align: center;'><p class='stat-number'>2 min</p><p class='stat-label'>To Full Competitor Report</p></div>", unsafe_allow_html=True)
with s3:
    st.markdown("<div style='text-align: center;'><p class='stat-number'>PayPal</p><p class='stat-label'>Secure Payments</p></div>", unsafe_allow_html=True)
with s4:
    st.markdown("<div style='text-align: center;'><p class='stat-number'>14 Days</p><p class='stat-label'>Free Trial</p></div>", unsafe_allow_html=True)
st.divider()

# --- FEATURE GRID ---
st.markdown("<h2 style='text-align: center; margin-bottom: 1.5rem;'>Competitive Advantage Built-In</h2>", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3)

with f1:
    st.markdown(f"""
    <div class="feature-card">
        <h3>{Icons.PRICING} Pricing Alerts</h3>
        <p class="text-muted">Receive alerts when rivals update their tiers, prices, or promotion packages.</p>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown(f"""
    <div class="feature-card">
        <h3>{Icons.REVIEWS} Sentiment Intelligence</h3>
        <p class="text-muted">Analyze customer sentiment across major review platforms to pinpoint rival weaknesses.</p>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown(f"""
    <div class="feature-card">
        <h3>{Icons.TRENDING_UP} Historical Audits</h3>
        <p class="text-muted">Analyze price evolution trends across time to predict market movements.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.divider()

# --- CALL TO ACTION ---
st.markdown("<h2 style='text-align: center;'>Ready to transform your research?</h2>", unsafe_allow_html=True)
_, footer_cta, _ = st.columns([1, 1.2, 1])
with footer_cta:
    if st.button("Create Account", type="primary", width='stretch'):
        st.switch_page("pages/02_Register.py")