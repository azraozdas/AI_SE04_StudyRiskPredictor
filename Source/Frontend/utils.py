import streamlit as st


def render_html(html: str) -> None:
    """Render a raw HTML fragment in the current Streamlit container."""
    st.markdown(html, unsafe_allow_html=True)