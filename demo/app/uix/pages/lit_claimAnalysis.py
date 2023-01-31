#--- about page
import streamlit as st
import pandas as pd
import plotly.express as px

import lib.claims as libClaims

description = "Claim Analysis"

def run():
    #--- page settings
    st.header("Claims Analysis")

    #--- raw claims data analysis
    dfClaims = libClaims.loadPkl_testClaims()
    st.dataframe(dfClaims)


    #--- bar charts
    col1, col2 = st.columns(2)

    #--- $claims reimbursed by provider
    pdfTopClaimsByProv = dfClaims.nlargest(10, "InscClaimAmtReimbursed")
    fig = px.bar(pdfTopClaimsByProv,
        x="Provider", y="InscClaimAmtReimbursed", title="$ Claims by Provider")
    col1.plotly_chart(fig, use_container_width=True)

    #--- #claims reimbursed by provider
    #pdfMaxClaimsByProv = dfClaims.groupby(['Provider'])['ClaimID'].count()
    pdfClaimCountByProv = dfClaims.groupby(
        by=["Provider"], as_index=False).agg(
            {"ClaimID": "count"}
        )    
    pdfClaimCountByProv = pdfClaimCountByProv.nlargest(10, "ClaimID")

    fig = px.bar(pdfClaimCountByProv,
        x="Provider", y="ClaimID", title="# Claims by Provider", barmode="group")
    col2.plotly_chart(fig, use_container_width=True)


    #---
    pdfDedAmtPaid = dfClaims.nlargest(10, "DeductibleAmtPaid")
    fig = px.bar(pdfDedAmtPaid,
        x="Provider", y="DeductibleAmtPaid", title="Deductible Paid by Provider")
    col1.plotly_chart(fig, use_container_width=True)