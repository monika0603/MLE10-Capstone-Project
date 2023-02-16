'''
    toExecute:  (from root app folder) ... streamlit run lit_index.py
'''
import streamlit as st
#from uix import lit_sidebar as lit_sideBar
import uix.lit_sidebar as litSideBar


#--- streamlit:  specify title and logo
st.set_page_config(
            page_title='Healthcare Claims - ML Anomaly Detection', 
            #page_icon='https://cdn.freebiesupply.com/logos/thumbs/1x/nvidia-logo.png', 
            layout="wide")
st.header("Healthcare ML Claims Anomaly Detection")
st.markdown('---')


#--- streamlit:  add a sidebar 
litSideBar.init()


#if __name__ == '__main__':
#    st.run("main:app", host="0.0.0.0", port=48300, reload=True)

#aryPkg[moduleNames.index(page)].run()