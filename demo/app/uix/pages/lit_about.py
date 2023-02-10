#--- about page
import streamlit as st

description = "About"
def run():

    print("\nINFO (lit_about.run)  loading ", description, " page ...") 

    #--- 
    st.experimental_memo.clear()            #--- try to clear cache each time this page is hit

    st.markdown('### About')
    st.markdown('<why this is important> ...')
    st.markdown('Kaggle Claims Data - (assume 2022)')
    st.markdown(
        """
            About page
        """,
            unsafe_allow_html=True,
        )