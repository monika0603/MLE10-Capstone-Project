import streamlit as st
import importlib
#import uix as libUix                    # default library name for apps
from uix import lit_packages
#from uix import pages as libUixPages

import uix.pages.lit_about
import uix.pages.lit_claimAnalysis
import uix.pages.lit_claimAnomalies


#--- alt define sidebar pages
m_aryPages = {
    "Home": uix.pages.lit_about,                            #--- TODO:  update
    "Claims Analysis": uix.pages.lit_claimAnalysis,
    "Anomaly Detection": uix.pages.lit_claimAnomalies,
    "Model - GBC": uix.pages.lit_claimAnalysis,             #--- TODO:  update
    "Model - Txf": uix.pages.lit_claimAnalysis,             #--- TODO:  update
    "About": uix.pages.lit_about
}


#--- define module-level vars
m_aryModNames = lit_packages.packages()
m_aryDescr = [] 
m_aryMods = []

def init():
    #--- upper panel
    with st.sidebar:
        kstrUrl_image = "data:image/png;base64,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"
        st.sidebar.image(kstrUrl_image, width=200)
        st.sidebar.markdown('Visualize Claims data Trends and Patterns over a given time span.') 
 
    #--- init select box
    #init_selectBox()

    #--- init checkboxes
    strKey = st.sidebar.radio("Go to", list(m_aryPages.keys()))
    pagSel = m_aryPages[strKey]
    writePage(pagSel)



def init_selectBox():
    #--- init module array of page names, and descr
    init_modDescrAry()

    # Display the sidebar with a menu of apps
    kstrMsg = """
            __Claims Anomaly Views__
            """
    with st.sidebar:
        st.markdown('---')
        st.markdown(kstrMsg)
        page = st.selectbox('Select:', m_aryModNames, format_func=fmt_modName) 

    #--- display sidebar footer
    with st.sidebar:
        st.markdown('---')
        st.write('Developed by Chavarria, McKone, Sharma')
        st.write('Contact at iain.mckone@gmail.com')
    
    # Run the chosen app
    m_aryMods[m_aryModNames.index(page)].run()



def init_modDescrAry():
    #--- init global array of page names, and descr
    #--- note:  you need to specify global scope for fxns to access module-level variables 
    global m_aryMods
    global m_aryDescr

    m_aryMods = []
    m_aryDescr = []
    for modName in m_aryModNames:
        modTemp = importlib.import_module('.'+modName,'uix')
        m_aryMods.append(modTemp)

        #--- If the module has a description attribute use that in the 
        #--- select box otherwise use the module name
        try:
            m_aryDescr.append(modTemp.description)
        except:
            m_aryDescr.append(modName)



#--- display the app descriptions instead of the module names in the selctbox
def fmt_modName(strName):
    global m_aryModNames
    global m_aryDescr
    return m_aryDescr[m_aryModNames.index(strName)]



def writePage(uixFile):  
    #--- writes out the page for the selected combo
  
    # _reload_module(page)
    uixFile.run()
