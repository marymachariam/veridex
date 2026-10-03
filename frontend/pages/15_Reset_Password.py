import requests
import streamlit as st

from config import settings, Icons
from components.chatbot import render_chatbot

st.set_page_config(page_title=f"{settings.APP_NAME} - Reset Password", layout="centered", initial_sidebar_state="collapsed")
render_chatbot()

st.markdown(f"# {Icons.COMPETITOR} Reset your password")

token = st.query_params.get("token")

if not token:
    st.error("Missing reset token. Use the link from your email.")
else:
    with st.form("reset_form"):
        new_password = st.text_input("New password", type="password")
        confirm_password = st.text_input("Confirm new password", type="password")
        submitted = st.form_submit_button("Reset Password", type="primary")

        if submitted:
            if not new_password or new_password != confirm_password:
                st.error("Passwords must match and not be empty.")
            else:
                try:
                    resp = requests.post(
                        f"{settings.API_BASE_URL}/api/v1/auth/reset-password",
                        json={"token": token, "new_password": new_password},
                        timeout=15,
                    )
                except requests.RequestException:
                    resp = None

                if resp is not None and resp.status_code == 200:
                    st.success("Password reset! You can now log in.")
                    st.page_link("pages/01_Login.py", label="Go to Login →")
                else:
                    try:
                        detail = resp.json().get("detail", "Reset failed.") if resp else "Could not reach the server."
                    except Exception:
                        detail = "Reset failed."
                    st.error(detail)