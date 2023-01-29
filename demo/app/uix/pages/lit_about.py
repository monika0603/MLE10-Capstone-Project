#--- about page
import streamlit as st

description = "About"
def run():
    #--- 
    st.markdown('### About')
    st.markdown('<why this is important> ...')
    st.markdown('Kaggle Claims Data - (assume 2022)')
    st.markdown(
        """
            About page
        """,
            unsafe_allow_html=True,
        )