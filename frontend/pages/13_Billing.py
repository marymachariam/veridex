import time

import requests
import streamlit as st

from config import settings, Icons
from utils.theme import apply_theme
from components.chatbot import render_chatbot

st.set_page_config(page_title=f"{settings.APP_NAME} - Billing", layout="wide")
apply_theme()
render_chatbot()


if "token" not in st.session_state:
    st.switch_page("pages/01_Login.py")

headers = {"Authorization": f"Bearer {st.session_state.token}"}

st.markdown(f"#  Billing & Plans")

# Handle PayPal redirect back to this page (?paypal_status=success/cancelled)
params = st.query_params
if params.get("paypal_status") == "success":
    st.success("Payment approved! It may take a few seconds for your plan to activate.")
    st.query_params.clear()
elif params.get("paypal_status") == "cancelled":
    st.warning("PayPal checkout was cancelled.")
    st.query_params.clear()

# ---- Current status ----
try:
    resp = requests.get(f"{settings.API_BASE_URL}/api/v1/billing/status", headers=headers, timeout=settings.API_TIMEOUT)
    status = resp.json() if resp.status_code == 200 else {}
except requests.RequestException:
    status = {}

if status:
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Plan", status.get("plan", "trial").capitalize())
        col2.metric("Status", status.get("status", "unknown").capitalize())
        provider = status.get("provider")
        col3.metric("Payment Method", provider.upper() if provider else "—")

        if status.get("provider") == "paypal" and status.get("status") == "active":
            if st.button("Cancel PayPal Subscription"):
                cancel_resp = requests.post(
                    f"{settings.API_BASE_URL}/api/v1/billing/paypal/cancel", headers=headers, timeout=settings.API_TIMEOUT
                )
                if cancel_resp.status_code == 200:
                    st.success("Subscription cancelled.")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Could not cancel. Please try again.")

st.divider()

# ---- Plan picker ----
st.markdown("## Choose a Plan")

PLANS = [
    {"key": "starter", "name": "Starter", "usd": 19, "kes": 2500, "features": ["Up to 10 competitors", "AI research", "Comparison view"]},
    {"key": "pro", "name": "Pro", "usd": 49, "kes": 6500, "features": ["Unlimited competitors", "Battlecards", "Change alerts", "Priority support"]},
]

cols = st.columns(len(PLANS))
for col, plan in zip(cols, PLANS):
    with col:
        with st.container(border=True):
            st.markdown(f"### {plan['name']}")
            st.markdown(f"**${plan['usd']}/mo** (USD) · **KES {plan['kes']:,}/mo**")
            for f in plan["features"]:
                st.write(f"✓ {f}")

            st.write("")
            tab_paypal, tab_mpesa = st.tabs(["Pay with PayPal", "Pay with M-Pesa"])

            with tab_paypal:
                if st.button(f"Subscribe via PayPal", key=f"paypal_{plan['key']}", type="primary", width='stretch'):
                    with st.spinner("Redirecting to PayPal..."):
                        try:
                            r = requests.post(
                                f"{settings.API_BASE_URL}/api/v1/billing/paypal/subscribe",
                                json={"plan": plan["key"]},
                                headers=headers,
                                timeout=30,
                            )
                        except requests.RequestException:
                            st.error("Could not reach the server.")
                            r = None

                    if r is not None:
                        if r.status_code == 200:
                            approval_url = r.json()["approval_url"]
                            st.markdown(f"[Click here to complete payment on PayPal →]({approval_url})")
                            st.link_button("Go to PayPal", approval_url, width='stretch')
                        else:
                            try:
                                detail = r.json().get("detail", "Could not start checkout.")
                            except Exception:
                                detail = "Could not start checkout."
                            st.error(detail)

            with tab_mpesa:
                phone = st.text_input("M-Pesa phone number", placeholder="0712345678", key=f"phone_{plan['key']}")
                if st.button(f"Pay with M-Pesa", key=f"mpesa_{plan['key']}", type="primary", width='stretch'):
                    if not phone:
                        st.error("Enter your phone number.")
                    else:
                        with st.spinner("Sending M-Pesa prompt to your phone..."):
                            try:
                                r = requests.post(
                                    f"{settings.API_BASE_URL}/api/v1/billing/mpesa/stk-push",
                                    json={"plan": plan["key"], "phone_number": phone},
                                    headers=headers,
                                    timeout=30,
                                )
                            except requests.RequestException:
                                st.error("Could not reach the server.")
                                r = None

                        if r is not None:
                            if r.status_code == 200:
                                st.success(r.json()["message"])
                                st.caption("Refresh this page after paying to see your updated plan status.")
                            else:
                                try:
                                    detail = r.json().get("detail", "Could not start M-Pesa payment.")
                                except Exception:
                                    detail = "Could not start M-Pesa payment."
                                st.error(detail)