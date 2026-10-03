"""
Chart components for data visualization
Line, bar, pie charts with professional styling
"""

import streamlit as st
import plotly.express as px
from config import Colors


def render_line_chart(data, x_col: str, y_col: str, title: str = ""):
    """
    Render a line chart
    
    Args:
        data: DataFrame
        x_col: X-axis column
        y_col: Y-axis column
        title: Chart title
    """
    fig = px.line(data, x=x_col, y=y_col, title=title)
    
    fig.update_traces(line_color=Colors.ACCENT_BLUE)
    fig.update_layout(
        height=300,
        margin=dict(t=30, b=0, l=0, r=0),
        hovermode="x unified"
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_bar_chart(data, x_col: str, y_col: str, title: str = ""):
    """
    Render a bar chart
    
    Args:
        data: DataFrame
        x_col: X-axis column
        y_col: Y-axis column
        title: Chart title
    """
    fig = px.bar(data, x=x_col, y=y_col, title=title)
    
    fig.update_traces(marker_color=Colors.ACCENT_BLUE)
    fig.update_layout(
        height=300,
        margin=dict(t=30, b=0, l=0, r=0),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_pie_chart(data, values_col: str, names_col: str, title: str = ""):
    """
    Render a pie chart
    
    Args:
        data: DataFrame
        values_col: Values column
        names_col: Names column
        title: Chart title
    """
    fig = px.pie(data, values=values_col, names=names_col, title=title)
    
    fig.update_layout(
        height=300,
        margin=dict(t=30, b=0, l=0, r=0)
    )
    
    st.plotly_chart(fig, use_container_width=True)