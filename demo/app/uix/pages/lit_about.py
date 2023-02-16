#--- about page
import streamlit as st

description = "About"
def run():

    print("\nINFO (lit_about.run)  loading ", description, " page ...") 

<<<<<<< HEAD
=======
    #--- 
    #st.experimental_memo.clear()            #--- try to clear cache each time this page is hit
    #st.cache_data.clear()
>>>>>>> 360355b48983568e01bd0e2968ae582d642a3e3d

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