"""
Streamlit Web App for Route Optimizer.
Embeds the real-time road-following, compiled Cython C++ Dijkstra navigation suite
with liquid glassmorphic floating controls.

Run with Streamlit:
    streamlit run dijkstra_c_vs_python/streamlit_app.py
"""

import os
import sys

# Ensure local dijkstra_c_vs_python directory is in python module path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import streamlit.components.v1 as components
from app import get_html_content


def main():
    st.set_page_config(
        page_title="Select Route · Route Optimizer",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Edge-to-edge styling for full immersion
    st.markdown(
        """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .block-container {
                padding: 0 !important;
                margin: 0 !important;
                max-width: 100% !important;
                height: 100vh !important;
            }
            iframe {
                border: none !important;
                width: 100vw !important;
                height: 98vh !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    html_code = get_html_content()
    components.html(html_code, height=940, scrolling=False)


if __name__ == "__main__":
    main()

