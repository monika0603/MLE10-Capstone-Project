from sklearn.cluster import KMeans
import lib.utils as libPaths
import pickle
import pandas as pd


m_kstrFile = __file__
m_kstrDataPath = libPaths.pth_data
m_kstrBinModelPath = libPaths.pth_binModels
m_kstrPcaModelPath = m_kstrBinModelPath + 'pca_kmeans_unsuperv_colab.pkl'
m_kstrKmeansModelPath = m_kstrBinModelPath + 'kmeans_unsuperv_colab.pkl'
m_blnTraceOn = True


#--- unsupervised:  Logistic Regession
def load_pcaFromPkl():
    with open(m_kstrPcaModelPath, 'rb') as filPkl:
        mdlAnoms = pickle.load(filPkl)
    return mdlAnoms


#--- unsupervised:  KMeans
def load_kmeansFromPkl():
    with open(m_kstrKmeansModelPath, 'rb') as filPkl:
        mdlAnoms = pickle.load(filPkl)
    return mdlAnoms


def save_pcaToPkl(mdlAnoms):
    with open(m_kstrPcaModelPath, 'wb') as filPkl:
        pickle.dump(mdlAnoms, filPkl)
    return mdlAnoms


def save_kmeansToPkl(mdlAnoms):
    with open(m_kstrKmeansModelPath, 'wb') as filPkl:
        pickle.dump(mdlAnoms, filPkl)
    return mdlAnoms



#--- determine which points can be labelled against which clusters
def predict(pdfScaled):
    #--- load a persisted fit kmeans model
    #--- predict will assign labels onto a similarly scaled data frame 


    #--- Note:  reverse chron through the code ...
    #---        4. KMeans was fit on X-reduced (22 cols)
    #---        3. X_reduced was a reduced column set of X-scaled (27 -> 22;  Dropped 5 cols:  DeadOrNot; and hotEncoded Gender and Race)
    #---        2. x_scaled was transformed through stdScaler
    #---        1. StdScaler was fit on X to produce X-scaled (X has 27 cols)
    pdfReduced = pdfScaled[['InscClaimAmtReimbursed', 'DeductibleAmtPaid',
        'AdmittedDays', 'RenalDiseaseIndicator', 'NoOfMonths_PartACov',
        'NoOfMonths_PartBCov', 'ChronicCond_Alzheimer',
        'ChronicCond_Heartfailure', 'ChronicCond_KidneyDisease',
        'ChronicCond_Cancer', 'ChronicCond_ObstrPulmonary',
        'ChronicCond_Depression', 'ChronicCond_Diabetes',
        'ChronicCond_IschemicHeart', 'ChronicCond_Osteoporasis',
        'ChronicCond_rheumatoidarthritis', 'ChronicCond_stroke',
        'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
        'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Age']]

    #--- prefit Kmeans clustering - was fit on trained pdfReduced
    #--- Note:  if we want to understand how kmeans performs on test/prod data, we need to predict
    mdlKMeans = load_kmeansFromPkl()
    ndaPredict = mdlKMeans.predict(pdfScaled)
#    ndaPredict = mdlKMeans.predict(pdfReduced)         #ValueError: X has 22 features, but KMeans is expecting 27 features as input.
    return ndaPredict


#--- feat eng
def do_featEng(pdfLoaded, blnIsTrain=False, hasGroupByProviderCols=True):
    print("INFO (mdl_kmeans.doFeatEng):  blnIsTrain, ", blnIsTrain)

    #--- columns_to_remove
    aryColsToDrop = ['BeneID', 'ClaimID', 'ClaimStartDt','ClaimEndDt','AttendingPhysician',
                     'OperatingPhysician', 'OtherPhysician', 'ClmDiagnosisCode_1',
                     'ClmDiagnosisCode_2', 'ClmDiagnosisCode_3', 'ClmDiagnosisCode_4',
                     'ClmDiagnosisCode_5', 'ClmDiagnosisCode_6', 'ClmDiagnosisCode_7',
                     'ClmDiagnosisCode_8', 'ClmDiagnosisCode_9', 'ClmDiagnosisCode_10',
                     'ClmProcedureCode_1', 'ClmProcedureCode_2', 'ClmProcedureCode_3',
                     'ClmProcedureCode_4', 'ClmProcedureCode_5', 'ClmProcedureCode_6',
                     'ClmAdmitDiagnosisCode', 'AdmissionDt',
                     'DischargeDt', 'DiagnosisGroupCode','DOB', 'DOD',
                     'State', 'County']
    pdfFeatEng = pdfLoaded.drop(columns=aryColsToDrop, axis=1)

    #--- flag categorical cols
    pdfFeatEng.Gender = pdfFeatEng.Gender.astype('category')
    pdfFeatEng.Race = pdfFeatEng.Race.astype('category')

    #--- one-hot-encoding
    pdfFeatEng = pd.get_dummies(pdfFeatEng, columns=['Gender', 'Race'], drop_first=True)
    if (blnIsTrain):
        #--- one-hot encode the potential fraud column (for training data only)
        try:
            #print("INFO (claims.doFeatEng):  one-hot encoding potential fraud")
            pdfFeatEng.loc[pdfFeatEng['PotentialFraud'] == 'Yes', 'PotentialFraud'] = 1
            pdfFeatEng.loc[pdfFeatEng['PotentialFraud'] == 'No', 'PotentialFraud'] = 0
        except KeyError:
            #--- likely column not found; invalid fxn call
            print("ERROR (claims.doFeatEng):  Potential Fraud col not found")

    pdfFeatEng.loc[pdfFeatEng['RenalDiseaseIndicator'] == 'Y', 'RenalDiseaseIndicator'] = 1 
    pdfFeatEng['DeductibleAmtPaid'].fillna(0, inplace=True)
    pdfFeatEng['AdmittedDays'].fillna(0, inplace=True)

    #--- check for correlated cols

    #--- add new features to assist with predictions
    if (hasGroupByProviderCols):
        pdfFeatEng['InscClaimReimbursement_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['InscClaimAmtReimbursed'].transform('mean') 
        pdfFeatEng['DeductibleAmtPaid_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['DeductibleAmtPaid'].transform('mean')
        
        pdfFeatEng['IPAnnualReimbursementAmt_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['IPAnnualReimbursementAmt'].transform('mean')
        pdfFeatEng['IPAnnualDeductibleAmt_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['IPAnnualDeductibleAmt'].transform('mean')

        pdfFeatEng['OPAnnualReimbursementAmt_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['OPAnnualReimbursementAmt'].transform('mean')
        pdfFeatEng['OPAnnualDeductibleAmt_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['OPAnnualDeductibleAmt'].transform('mean')
    return pdfFeatEng


def fit(pdfScaled):
    #--- determine the centroids of the kmeans clusters
    #--- refit kmeans clustering according to the pre-scaled data provided
    #--- note:  this all assumes that the nature of the data and the number of clusters remain unchanged
    m_klngNumClusters = 3
    if (m_blnTraceOn): print("TRACE (" + m_kstrFile + ".fit)  instantiate KMeans ...")
    mdlKMeans = KMeans(n_clusters=m_klngNumClusters, max_iter=50, random_state=2022)            #--- #clusters was learned from training    
    
    if (m_blnTraceOn): print("TRACE (" + m_kstrFile + ".fit)  fitting data (scaled) ...")
    mdlKMeans.fit(pdfScaled)           #--- fit on test/prod data
    
    return mdlKMeans                    #--- this ibject will give us all results based on kmeans


def train(pdfTrainData):
    mdlAnoms = KMeans(n_clusters=3, max_iter=50, random_state=2022)
    mdlAnoms.fit(pdfTrainData.values)
    save_kmeansToPkl(mdlAnoms)
    return mdlAnoms