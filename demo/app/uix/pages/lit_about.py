#--- about page
import streamlit as st

description = "About"
def run():

    print("\nINFO (lit_about.run)  loading ", description, " page ...") 


    st.markdown('### About')
    st.markdown('### MLE10 Capstone:  Healthcare Anomaly Detection')
    st.markdown('#### Team:  McKone, Sharma, Chavarria, Lederer')

    st.markdown('Kaggle Claims Data:')
    st.markdown('https://www.kaggle.com/code/rohitrox/medical-provider-fraud-detection/data')
    st.markdown(
        """
            About page
        """,
            unsafe_allow_html=True,
        )