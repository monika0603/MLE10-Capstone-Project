#--- anomaly detection - supervised page
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import lib.claims as libClaims

description = "Anomaly Detection - Supervised"
m_kbln_traceOn = False                                  #--- enable/disable module level tracing

def run():
    #--- note:  in python, you need to specify global scope for fxns to access module-level variables 
    global m_kbln_traceOn

    try:

        #--- page settings
        if (m_kbln_traceOn):  print("TRACE (litAnomSuperv.run):  Initialize Page Settings ...")
        st.header("_Provider_ Anomalies - Supervised Approach (GBC)")


        #--- show:  raw claims data analysis
        if (m_kbln_traceOn):  print("TRACE (litAnomSuperv.run):  Show Raw Claims Dataframe ...")
        dfClaims = libClaims.load_claims(False)
        dfPred = libClaims.get_gbcPredict(dfClaims) 

        dfSample = dfPred.sample(50)
    
        #dfTopClaims = dfPred.nlargest(25, "InscClaimAmtReimbursed")
        dfTopClaims = dfSample.sort_values(by=["InscClaimAmtReimbursed"], ascending=False)
        dfAnoms = dfTopClaims[dfTopClaims['hasAnom?'] > 0] 

        #--- show $claims reimbursed by provider
        if (m_kbln_traceOn):  print("TRACE (litAnomSuperv.run):  Show $claims reimbursed by provider ...")
        pdfTopClaimsByProv = dfTopClaims
        st.markdown("(Top) Ins Reimbursed by Provider")
        st.dataframe(pdfTopClaimsByProv)

        st.markdown("(Sample) Provider Anomalies Claims Data:  Providers, Beneficiaries, Physicians, Procedures, etc")
        st.dataframe(dfAnoms)

        fig = go.Figure(
            layout=dict(
                #xaxis=dict(categoryorder="category descending"),
                #yaxis=dict(range=[0, 7]),
                #scattermode="group",
                legend=dict(groupclick="toggleitem"),
            )
        )

        fig.add_trace(
            go.Bar(
                x=pdfTopClaimsByProv.Provider,
                y=pdfTopClaimsByProv.InscClaimAmtReimbursed,
                name="Ins Claims Reibursed",
                marker_color="IndianRed",
                #offsetgroup="anoms",
                #legendgroup="anoms",
                #legendgrouptitle_text="Anoms",
            )
        )

        
        fig.add_trace(
            go.Scatter(
                x=dfAnoms.Provider,
                y=dfAnoms.InscClaimAmtReimbursed,
                mode="markers",
                marker = dict(size = 15, color = 'red', symbol = 'cross'),
                #offsetgroup="anoms",
                #legendgroup="anoms",
                name="Anomalies"
            )) 

        st.plotly_chart(fig, use_container_width=True)

    except TypeError as e:
        print("ERROR (litAnomSuperv.run):  ", e)