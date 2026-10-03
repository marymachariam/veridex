import streamlit as st

from config import Icons


def render_report(report: dict):
    st.markdown(f"## {report['name']}")
    meta = " · ".join(filter(None, [report.get("category"), report.get("website"), str(report.get("founded_year") or "")]))
    if meta:
        st.caption(meta)

    insight = report.get("insight") or {}
    if insight.get("tagline"):
        st.markdown(f"**Positioning:** {insight['tagline']}")
    if insight.get("summary"):
        st.write(insight["summary"])
    if insight.get("target_market"):
        st.markdown(f"**Target market:** {insight['target_market']}")

    st.markdown("### Pricing")
    if report.get("pricing"):
        for tier in report["pricing"]:
            price = f"${tier['price_usd']:,.0f}/{tier['billing_period']}" if tier.get("price_usd") is not None else "Contact sales"
            st.write(f"**{tier['tier_name']}** — {price}")
    else:
        st.caption("No pricing found.")

    st.markdown("### Key Features")
    if report.get("features"):
        st.write(", ".join(f["feature_name"] for f in report["features"]))
    else:
        st.caption("No features found.")

    st.markdown("### SWOT")
    swot_cols = st.columns(4)
    labels = [("strengths", "Strengths"), ("weaknesses", "Weaknesses"), ("opportunities", "Opportunities"), ("threats", "Threats")]
    for col, (key, label) in zip(swot_cols, labels):
        with col:
            st.markdown(f"**{label}**")
            for item in (insight.get(key) or "").split("\n"):
                if item.strip():
                    st.write(f"- {item.strip()}")

    if insight.get("recent_signals"):
        st.markdown("### Recent Signals")
        for item in insight["recent_signals"].split("\n"):
            if item.strip():
                st.write(f"- {item.strip()}")

    if insight.get("sources"):
        with st.expander("Sources"):
            for src in insight["sources"].split("\n"):
                if src.strip():
                    st.write(src.strip())