#--- claim analysis page
import streamlit as st
import pandas as pd
import plotly.express as px

import lib.claims as libClaims

description = "Claim Analysis"
m_kbln_traceOn = False                                  #--- enable/disable module level tracing


def run():
    #--- note:  in python, you need to specify global scope for fxns to access module-level variables 
    global m_kbln_traceOn

    try:

        #--- page settings
        if (m_kbln_traceOn):  print("TRACE (litClaimAnalysis.run):  Initialize Page Settings ...")
        st.header("Claims Analysis")


        #--- show:  raw claims data analysis
        if (m_kbln_traceOn):  print("TRACE (litClaimAnalysis.run):  Show Raw Claims Dataframe ...")
        dfClaims = libClaims.load_claims(False) 
        #dfClaims = libClaims.loadPkl_testClaims()       #--- note:  a large dataset;  reduce before render
        dfRaw = dfClaims.sample(25)
        st.markdown("(Sample) Raw Claims Data:  Providers, Beneficiaries, Physicians, Procedures, etc")
        st.dataframe(dfRaw)


        #--- show:  data grouped by provider
        pdfClaimsByProvider = dfClaims.groupby(
            by=["Provider"], as_index=False).agg(
                {"ClaimID":"count", "InscClaimAmtReimbursed":"sum", "DeductibleAmtPaid":"sum"}
            )    
        st.markdown("(Sample) Raw Claims Data:  Grouped by Provider")
        st.dataframe(pdfClaimsByProvider.sample(25))

        #--- show:  bar charts
        col1, col2 = st.columns(2)

        #--- show $claims reimbursed by provider
        if (m_kbln_traceOn):  print("TRACE (litClaimAnalysis.run):  Show $claims reimbursed by provider ...")
        pdfTopClaimsByProv = dfClaims.nlargest(10, "InscClaimAmtReimbursed")
        fig = px.bar(pdfTopClaimsByProv,
            x="Provider", y="InscClaimAmtReimbursed", title="$ Claims by Provider")
        #col1.markdown("(Sample) $Claims Reimbursed by Provider")
        col1.plotly_chart(fig, use_container_width=True)

        #--- #claims reimbursed by provider
        if (m_kbln_traceOn):  print("TRACE (litClaimAnalysis.run):  Show #claims reimbursed by provider ...")
        #pdfMaxClaimsByProv = dfClaims.groupby(['Provider'])['ClaimID'].count()
        pdfClaimCountByProv = dfClaims.groupby(
            by=["Provider"], as_index=False).agg(
                {"ClaimID": "count"}
            )    
        pdfClaimCountByProv = pdfClaimCountByProv.nlargest(10, "ClaimID")
        fig = px.bar(pdfClaimCountByProv,
            x="Provider", y="ClaimID", title="# Claims by Provider", barmode="group")
        #col2.markdown("(Sample) #Claims Reimbursed by Provider")           #--- just to even out the display
        col2.plotly_chart(fig, use_container_width=True)


        #--- TODO:  (optimization) create a single group by dataframe;  try not to recreate for each chart 
        if (m_kbln_traceOn):  print("TRACE (litClaimAnalysis.run):  Show top $deductible paid by provider ...")
        pdfDedAmtPaid = dfClaims.nlargest(10, "DeductibleAmtPaid")
        fig = px.bar(pdfDedAmtPaid,
            x="Provider", y="DeductibleAmtPaid", title="Deductible Paid by Provider")
        col1.plotly_chart(fig, use_container_width=True)
    
        if (m_kbln_traceOn):  print("TRACE (litClaimAnalysis.run):  end of fxn ...")

    except TypeError as e:
        print("ERROR (litClaimAnalysis.run):  ", e)