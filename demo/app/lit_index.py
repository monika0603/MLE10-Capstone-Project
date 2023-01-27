'''
    toExecute:  (from root app folder) ... streamlit run lit_index.py
'''

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

import pandas as pd

import lib.claims as libClaims

#--- get the dataframe
pdfClaims = libClaims.loadPkl_testClaims()


#--- streamlit:  specify title and logo
st.set_page_config(page_title='Healthcare ML Claims Anomaly Detection:  ', 
page_icon='https://cdn.freebiesupply.com/logos/thumbs/1x/nvidia-logo.png', layout="wide")


#--- streamlit:  add a sidebar 
st.markdown('---')
st.sidebar.image('https://cdn.freebiesupply.com/logos/thumbs/1x/nvidia-logo.png', width=200)
st.sidebar.markdown('# Healthcare ML Claims Anomaly Detection')
st.sidebar.markdown('Anomaly Detection, Automation is awesome ...')
st.sidebar.markdown('Kaggle Claims Data - (imagine for 2022)')
st.sidebar.markdown('Visualise Claims data Trends and Patterns over a given time span.') 

st.sidebar.markdown('---')
st.sidebar.write('Developed by Chavarria, McKone, Sharma')
st.sidebar.write('Contact at iain.mckone@gmail.com')


#rteClaims = APIRouter()