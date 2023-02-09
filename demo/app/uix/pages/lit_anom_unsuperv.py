#--- anomaly detection - unsupervised page
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

import lib.claims as libClaims
import lib.providers as libProviders
import lib.utils as libUtils

description = "Anomaly Detection - Unsupervised"
m_kbln_traceOn = False                                  #--- enable/disable module level tracing

def run():
    #--- note:  in python, you need to specify global scope for fxns to access module-level variables 
    global m_kbln_traceOn

    try:

        #--- page settings
        if (m_kbln_traceOn):  print("TRACE (litAnomUnSuperv.run):  Initialize Page Settings ...")
        st.header("Claims Anomalies - Unsupervised Approach (KMeans)")

        #--- TODO:
        #prep a claims test data file
        #provide a file drag/drop

        #--- show:  raw claims data analysis
        if (m_kbln_traceOn):  print("TRACE (litAnomUnsuperv.run):  Show Raw Claims Dataframe ...")
        pdfClaims = libClaims.load_claims(False)


        #--- get unsupervised predictions
        #pdfFeatEng = libClaims.do_featEng(pdfClaims)
        pdfPred = libClaims.get_kmeansPredict(pdfClaims)
        pdfSample = pdfPred.sample(100)
        pdfSample['providerId'] = pdfSample['Provider'].str[3:].astype(np.float64)


        #--- save this file locally as a pkl
        """         from datetime import date
                import time
                strDteNow = date.today().strftime('%Y%m%d')
                strTimeNow = time.strftime('%H%M%S')
                strProvTestFile = libUtils.pth_data + strDteNow + strTimeNow + "_claimsTestSample.pkl"
                pd.to_pickle(pdfClaims.sample(50), strProvTestFile) """


        #--- table of claims and clusters, sorted by InscClaimAmt Reimbursed
        pdfTopClaims = pdfSample.sort_values(by=["cluster", "InscClaimAmtReimbursed"], ascending=False)
        if (m_kbln_traceOn):  print("TRACE (litAnomUnsuperv.run):  Show $claims reimbursed by cluster ...")
        st.markdown("(Top) Ins Claim Reimbursed by Cluster")
        st.dataframe(pdfTopClaims)

        
        #--- chart cluster data distribution
        chart_clusterDistr(pdfSample)


        col1, col2 = st.columns(2)


        #--- chart KMeans clusters")
        chart_KMeansClusters(pdfSample, "Age", "InscClaimAmtReimbursed", col1)


        #--- chart KMeans clusters")
        chart_KMeansClusters(pdfSample, "providerId", "InscClaimAmtReimbursed", col2)


    except TypeError as e:
        print("ERROR (litAnomSuperv.run):  ", e)


def chart_clusterDistr(pdfSample):
    pdfClustDistr = pdfSample['cluster'].value_counts()

    fig = go.Figure(
        layout=dict(
            legend=dict(groupclick="toggleitem"),
            xaxis=dict(title='cluster'),
            yaxis=dict(title='#data points')
        )
    )

    fig.add_trace(
        go.Bar(
            x=pdfClustDistr.index,
            y=pdfClustDistr.values,
        )
    )
    st.plotly_chart(fig, use_container_width=True)


def chart_KMeansClusters(pdfSample, strXFeature, strYFeature, stCol):
    pdfScatter = pdfSample
    pdfCluster0 = pdfScatter[pdfScatter['cluster'] == 0] 
    pdfCluster1 = pdfScatter[pdfScatter['cluster'] == 1] 
    pdfCluster2 = pdfScatter[pdfScatter['cluster'] == 2] 

    kstrTitle = "(KMeans Clusters) Claims data"
    #--- chart 
    fig = go.Figure(
        layout=dict(
            legend=dict(groupclick="toggleitem"),
            xaxis=dict(title=strXFeature),
            yaxis=dict(title=strYFeature)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=pdfCluster0[strXFeature],
            y=pdfCluster0[strYFeature],
            text="claimId: " + pdfCluster0['ClaimID'],
            mode='markers',
            name='cluster0'
        )
    )

    fig.add_trace(
        go.Scatter(
            x=pdfCluster1[strXFeature],
            y=pdfCluster1[strYFeature],
            mode='markers',
            name='cluster1'
        )) 

    fig.add_trace(
        go.Scatter(
            x=pdfCluster2[strXFeature],
            y=pdfCluster2[strYFeature],
            mode='markers',
            name='cluster2'
        )) 
    stCol.plotly_chart(fig, use_container_width=True)
