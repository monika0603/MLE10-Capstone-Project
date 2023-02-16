#--- provider analysis page
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import lib.claims as libClaims
import lib.providers as libProviders

description = "Provider Analysis"
m_kbln_traceOn = False                                  #--- enable/disable module level tracing


def run():
    #--- note:  in python, you need to specify global scope for fxns to access module-level variables 
    global m_kbln_traceOn

    try:

        #--- page settings
        if (m_kbln_traceOn):  print("TRACE (litProviderAnalysis.run):  Initialize Page Settings ...")
        st.header("Provider Analysis")


        #--- show:  data grouped by provider
        pdfClaims = libClaims.load_claims(False) 
        pdfClaimsByProvider = pdfClaims.groupby(
            by=["Provider"], as_index=False).agg({
                "ClaimID":"count", 
                "InscClaimAmtReimbursed":"sum", 
                "DeductibleAmtPaid":"sum",
                "AdmittedDays":"count",
                "RenalDiseaseIndicator":"count",
                "ChronicCond_Alzheimer":"count",
                "ChronicCond_Heartfailure":"count",
                "ChronicCond_KidneyDisease":"count",
                "ChronicCond_Cancer":"count",
                "ChronicCond_ObstrPulmonary":"count",
                "IPAnnualDeductibleAmt":"sum",
                "Age":"mean"
                }
            )    
        st.markdown("(Sample) Raw Claims Data:  Grouped by Provider")
        st.dataframe(pdfClaimsByProvider.sample(50))


        #--- get supervised predictions
        pdfFeatEng = libClaims.do_featEng(pdfClaims)
        pdfPred = libProviders.get_xgbPredict(pdfFeatEng)
        dfSample = pdfPred.sample(50)
    
        #--- inspect top provider claims
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
                marker_color="Blue",
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
                marker = dict(size = 15, color = 'red', symbol = 'x'),
                #offsetgroup="anoms",
                #legendgroup="anoms",
                name="Anomalies"
            )) 

        st.plotly_chart(fig, use_container_width=True)


    except TypeError as e:
        print("ERROR (litAnomSuperv.run):  ", e)


        #--- show:  bar charts
        col1, col2 = st.columns(2)

        #--- show $claims reimbursed by provider
        if (m_kbln_traceOn):  print("TRACE (litClaimAnalysis.run):  Show $claims reimbursed by provider ...")
        pdfTopClaimsByProv = pdfClaims.nlargest(10, "InscClaimAmtReimbursed")
        fig = px.bar(pdfTopClaimsByProv,
            x="Provider", y="InscClaimAmtReimbursed", title="$ Claims by Provider")
        #col1.markdown("(Sample) $Claims Reimbursed by Provider")
        col1.plotly_chart(fig, use_container_width=True)

        #--- #claims reimbursed by provider
        if (m_kbln_traceOn):  print("TRACE (litClaimAnalysis.run):  Show #claims reimbursed by provider ...")
        #pdfMaxClaimsByProv = dfClaims.groupby(['Provider'])['ClaimID'].count()
        pdfClaimCountByProv = pdfClaims.groupby(
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
        pdfDedAmtPaid = pdfClaims.nlargest(10, "DeductibleAmtPaid")
        fig = px.bar(pdfDedAmtPaid,
            x="Provider", y="DeductibleAmtPaid", title="Deductible Paid by Provider")
        col1.plotly_chart(fig, use_container_width=True)
    
        if (m_kbln_traceOn):  print("TRACE (litClaimAnalysis.run):  end of fxn ...")

    except TypeError as e:
        print("ERROR (litClaimAnalysis.run):  ", e)