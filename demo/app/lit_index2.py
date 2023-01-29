'''
    toExecute:  (from root app folder) ... streamlit run lit_index.py
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime

import json
import streamlit as st
import importlib

import lib.claims as libClaims
import uix as libUix   # default library name for apps
from uix import lit_packages
from uix import lit_sidebar as lit_sideBar


#--- get the dataframe
pdfClaims = libClaims.loadPkl_testClaims()


#--- streamlit:  specify title and logo
st.set_page_config(
            page_title='Healthcare ML Claims Anomaly Detection:  ', 
            page_icon='https://cdn.freebiesupply.com/logos/thumbs/1x/nvidia-logo.png', 
            layout="wide")
st.header("National Statistics")
st.markdown('---')


#--- streamlit:  add a sidebar 
lit_sideBar.init()


'''

if __name__ == '__main__':
    st.run("main:app", host="0.0.0.0", port=48300, reload=True)
'''
#aryPkg[moduleNames.index(page)].run()