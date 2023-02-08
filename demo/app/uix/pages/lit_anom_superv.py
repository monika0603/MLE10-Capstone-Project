#--- anomaly detection - supervised page
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import lib.claims as libClaims
import lib.providers as libProviders
import lib.utils as libUtils

description = "Anomaly Detection - Supervised"
m_kbln_traceOn = False                                  #--- enable/disable module level tracing

def run():
    #--- note:  in python, you need to specify global scope for fxns to access module-level variables 
    global m_kbln_traceOn

    try:

        #--- page settings
        if (m_kbln_traceOn):  print("TRACE (litAnomSuperv.run):  Initialize Page Settings ...")
        st.header("Provider Anomalies - Supervised Approach (XG Boost)")

        #--- TODO:
        #prep a grouped test data file
        #provide a file drag/drop

        #--- show:  raw claims data analysis
        if (m_kbln_traceOn):  print("TRACE (litAnomSuperv.run):  Show Raw Claims Dataframe ...")
        pdfClaims = libClaims.load_claims(False)


        #--- get supervised predictions
        pdfFeatEng = libClaims.do_featEng(pdfClaims)
        pdfPred = libProviders.get_xgbPredict(pdfFeatEng)
        pdfSample = pdfPred.sample(50)


        #--- save this file locally as a pkl
        """         from datetime import date
                import time
                strDteNow = date.today().strftime('%Y%m%d')
                strTimeNow = time.strftime('%H%M%S')
                strProvTestFile = libUtils.pth_data + strDteNow + strTimeNow + "_provTestSample.pkl"
                pd.to_pickle(pdfClaims.sample(50), strProvTestFile) """
        

        #--- table sorted $insClaims reimbursed by provider
        #--- display providers with predictions, sorted by InscClaimAmt Reimbursed
        pdfTopClaims = pdfSample.sort_values(by=["InscClaimAmtReimbursed"], ascending=False)
        if (m_kbln_traceOn):  print("TRACE (litAnomSuperv.run):  Show $claims reimbursed by provider ...")
        st.markdown("(Top) Ins Reimbursed by Provider")
        st.dataframe(pdfTopClaims)


        #--- table filtered list of anomalies
        #st.markdown("(Sample) Provider Anomalies Claims Data:  Providers, Beneficiaries, Physicians, Procedures, etc")
        #st.dataframe(dfAnoms)


        #--- chart Top Insurance claims ($) by Provider")
        chart_topInsClaimsByProvider(pdfSample)


        #--- chart Top deductible amts ($) by Provider")
        chart_topDeductiblePaidByProvider(pdfSample)


        #--- chart Top IP Annual Reimbursement amts ($) by Provider")
        chart_topIPAnnualReimbAmtByProvider(pdfSample)


        #--- chart Top IP Annual Reimbursement amts ($) by Provider")
        chart_topIPAnnualDeductAmtByProvider(pdfSample)


        #--- chart Top IP Annual Reimbursement amts ($) by Provider")
        chart_topOPAnnualReimbAmtByProvider(pdfSample)


        #--- chart Top IP Annual Reimbursement amts ($) by Provider")
        chart_topOPAnnualDeductAmtByProvider(pdfSample)

    except TypeError as e:
        print("ERROR (litAnomSuperv.run):  ", e)



def chart_topOPAnnualReimbAmtByProvider(pdfSample):
    pdfBar = pdfSample.sort_values(by=["OPAnnualReimbursementAmt"], ascending=False)
    pdfAnoms = pdfBar[pdfBar['hasAnom?'] > 0] 

    #--- chart 
    fig = go.Figure(
        layout=dict(
            title="(Sample Anomalies) Top OP Reimb Paid ($) by Provider",
            legend=dict(groupclick="toggleitem"),
        )
    )

    fig.add_trace(
        go.Bar(
            x=pdfBar.Provider,
            y=pdfBar.OPAnnualReimbursementAmt,
            name="OP Reimb Paid",
            marker_color="LightBlue",
        )
    )

    
    fig.add_trace(
        go.Scatter(
            x=pdfAnoms.Provider,
            y=pdfAnoms.OPAnnualReimbursementAmt,
            mode="markers",
            marker = dict(size = 15, color = 'IndianRed', symbol = 'x'),
            name="Anomalies"
        )) 

    st.plotly_chart(fig, use_container_width=True)



def chart_topOPAnnualDeductAmtByProvider(pdfSample):
        pdfBar = pdfSample.sort_values(by=["OPAnnualDeductibleAmt"], ascending=False)
        pdfAnoms = pdfBar[pdfBar['hasAnom?'] > 0] 

        #--- chart 
        fig = go.Figure(
            layout=dict(
                title="(Sample Anomalies) Top OP Deduct Amt ($) by Provider",
                legend=dict(groupclick="toggleitem"),
            )
        )

        fig.add_trace(
            go.Bar(
                x=pdfBar.Provider,
                y=pdfBar.OPAnnualDeductibleAmt,
                name="OP Deductible Paid",
                marker_color="LightBlue",
            )
        )

        
        fig.add_trace(
            go.Scatter(
                x=pdfAnoms.Provider,
                y=pdfAnoms.OPAnnualDeductibleAmt,
                mode="markers",
                marker = dict(size = 15, color = 'IndianRed', symbol = 'x'),
                name="Anomalies"
            )) 

        st.plotly_chart(fig, use_container_width=True)



def chart_topIPAnnualReimbAmtByProvider(pdfSample):
        pdfBar = pdfSample.sort_values(by=["IPAnnualReimbursementAmt"], ascending=False)
        pdfAnoms = pdfBar[pdfBar['hasAnom?'] > 0] 

        #--- chart 
        fig = go.Figure(
            layout=dict(
                title="(Sample Anomalies) Top IP Reimb Paid ($) by Provider",
                legend=dict(groupclick="toggleitem"),
            )
        )

        fig.add_trace(
            go.Bar(
                x=pdfBar.Provider,
                y=pdfBar.IPAnnualReimbursementAmt,
                name="IP Reimb Paid",
                marker_color="LightBlue",
            )
        )

        
        fig.add_trace(
            go.Scatter(
                x=pdfAnoms.Provider,
                y=pdfAnoms.IPAnnualReimbursementAmt,
                mode="markers",
                marker = dict(size = 15, color = 'IndianRed', symbol = 'x'),
                name="Anomalies"
            )) 

        st.plotly_chart(fig, use_container_width=True)



def chart_topIPAnnualDeductAmtByProvider(pdfSample):
        pdfBar = pdfSample.sort_values(by=["IPAnnualDeductibleAmt"], ascending=False)
        pdfAnoms = pdfBar[pdfBar['hasAnom?'] > 0] 

        #--- chart 
        fig = go.Figure(
            layout=dict(
                title="(Sample Anomalies) Top IP Deduct Amt ($) by Provider",
                legend=dict(groupclick="toggleitem"),
            )
        )

        fig.add_trace(
            go.Bar(
                x=pdfBar.Provider,
                y=pdfBar.IPAnnualDeductibleAmt,
                name="IP Deductible Paid",
                marker_color="LightBlue",
            )
        )

        
        fig.add_trace(
            go.Scatter(
                x=pdfAnoms.Provider,
                y=pdfAnoms.IPAnnualDeductibleAmt,
                mode="markers",
                marker = dict(size = 15, color = 'IndianRed', symbol = 'x'),
                name="Anomalies"
            )) 

        st.plotly_chart(fig, use_container_width=True)


def chart_topDeductiblePaidByProvider(pdfSample):
        pdfBar = pdfSample.sort_values(by=["DeductibleAmtPaid"], ascending=False)
        pdfAnoms = pdfBar[pdfBar['hasAnom?'] > 0] 

        #--- chart 
        fig = go.Figure(
            layout=dict(
                title="(Sample Anomalies) Top Deductibles Paid ($) by Provider",
                legend=dict(groupclick="toggleitem"),
            )
        )

        fig.add_trace(
            go.Bar(
                x=pdfBar.Provider,
                y=pdfBar.DeductibleAmtPaid,
                name="Deductibles Paid",
                marker_color="LightBlue",
                #offsetgroup="anoms",
                #legendgroup="anoms",
                #legendgrouptitle_text="Anoms",
            )
        )

        
        fig.add_trace(
            go.Scatter(
                x=pdfAnoms.Provider,
                y=pdfAnoms.DeductibleAmtPaid,
                mode="markers",
                marker = dict(size = 15, color = 'IndianRed', symbol = 'x'),
                #offsetgroup="anoms",
                #legendgroup="anoms",
                name="Anomalies"
            )) 

        st.plotly_chart(fig, use_container_width=True)


def chart_topInsClaimsByProvider(pdfSample):
        pdfTopClaims = pdfSample.sort_values(by=["InscClaimAmtReimbursed"], ascending=False)
        pdfAnoms = pdfTopClaims[pdfTopClaims['hasAnom?'] > 0] 

        #--- chart 
        #st.markdown("(Sample Anomalies) Top Insurance claims ($) by Provider")
        fig = go.Figure(
            layout=dict(
                #xaxis=dict(categoryorder="category descending"),
                #yaxis=dict(range=[0, 7]),
                #scattermode="group",
                title="(Sample Anomalies) Top Insurance claims ($) by Provider",
                legend=dict(groupclick="toggleitem"),
            )
        )

        fig.add_trace(
            go.Bar(
                x=pdfTopClaims.Provider,
                y=pdfTopClaims.InscClaimAmtReimbursed,
                name="Ins Claims Reibursed",
                marker_color="LightBlue",
                #offsetgroup="anoms",
                #legendgroup="anoms",
                #legendgrouptitle_text="Anoms",
            )
        )

        
        fig.add_trace(
            go.Scatter(
                x=pdfAnoms.Provider,
                y=pdfAnoms.InscClaimAmtReimbursed,
                mode="markers",
                marker = dict(size = 15, color = 'IndianRed', symbol = 'x'),
                #offsetgroup="anoms",
                #legendgroup="anoms",
                name="Anomalies"
            )) 

        st.plotly_chart(fig, use_container_width=True)