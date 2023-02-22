#--- about page
import streamlit as st

description = "Home"
def run():

    print("\nINFO (lit_home.run)  loading ", description, " page ...") 


    st.markdown('### Home')
    st.markdown('### MLE10 Capstone:  Healthcare Anomaly Detection')
    st.markdown('\
        Healthcare fraud is an expensive white-collar crime in the US and leads to an \
        increase in healthcare premiums, and a reduction in quality and access to care.\
        The National Health Care Anti-Fraud Association conservatively estimates that \
        about 3 percent of US healthcare spending is lost to fraud per year ($300 billion \
        approximately).')
    
    st.markdown('\
        Machine Learning techniques can identify current and evolving anomalies in claims \
        data.  As fraud becomes more sophisticated across an increasing number of annual \
        transactions, an ML solution provides an opportunity to greatly reduce the effort, \
        time and associated cost spent in identifying claims anomalies, and recouping any \
        misappropriated funds. ')
    
    st.markdown('\
        To illustrate the capabilities of Machine Learning to identify claims anomalies, \
        this capstone project team has developed two solutions:  \
        \n\t - a supervised Logistic Regression Model to identify potential anomalies at \
             the provider level \
        \n\t - an unsupervised KMeans Clustering Model to identify potential anomalies \
                at the claim level.')

    st.markdown(
        """

            Home page
        
        """,
            unsafe_allow_html=True,
        )