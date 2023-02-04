import pandas as pd
import lib.utils as libPaths

from lib.models import mdl_utils, mdl_xgb, mdl_logR, mdl_svm
from lib.models import mdl_autoenc, mdl_kmeans


#--- load, merge data from file
m_kstrDataPath = libPaths.pth_data
m_kstrModelPath = libPaths.pth_model
m_kstrBinModelPath = libPaths.pth_binModels



def getPath_defPklClaims(blnIsTrain=False):
    global m_kstrDataPath
    strPrefix="test_"
    if (blnIsTrain):  strPrefix = "train_"
    strPth_pklClaims = m_kstrDataPath + strPrefix + 'claims.pkl'
    return strPth_pklClaims



def load_claims(blnIsTrain=False, blnForceCsv=False):
    if (blnForceCsv):  
        pdfClaims = loadCsv_claims(blnIsTrain)
    else:
        pdfClaims = loadPkl_claims(blnIsTrain)
    return pdfClaims



def loadCsv_claims(blnIsTrain=False):
    global m_kstrDataPath
    #--- load all csv test data
    if (blnIsTrain):
        print("INFO (loadCsv_claimsData):  load train data ...")
        strPthProvider = m_kstrDataPath + 'Train-1542865627584.csv'
        strPthBenef = m_kstrDataPath + 'Train_Beneficiarydata-1542865627584.csv'
        strPthInpat = m_kstrDataPath + 'Train_Inpatientdata-1542865627584.csv'
        strPthOutpat = m_kstrDataPath + 'Train_Outpatientdata-1542865627584.csv'
    else:
        print("INFO (loadCsv_claimsData):  load test data ...")
        strPthProvider = m_kstrDataPath + 'Test-1542969243754.csv'
        strPthBenef = m_kstrDataPath + 'Test_Beneficiarydata-1542969243754.csv'
        strPthInpat = m_kstrDataPath + 'Test_Inpatientdata-1542969243754.csv'
        strPthOutpat = m_kstrDataPath + 'Test_Outpatientdata-1542969243754.csv'
    
    #--- output:  pandas data frame
    pdfProvider = pd.read_csv(strPthProvider) 
    pdfBenef = pd.read_csv(strPthBenef)
    pdfInpat = pd.read_csv(strPthInpat)
    pdfOutpat = pd.read_csv(strPthOutpat) 

    #--- data engineering 
    pdfBenef = prep_benefData(pdfBenef)
    pdfInpat = prep_inpatData(pdfInpat)

    #--- merge inpatient and outpatient data (assert: 31 cols)
    aryMergeCols = list(pdfOutpat.columns)
    pdfAllpat = pdfInpat.merge(pdfOutpat, on=aryMergeCols, how='outer')

    #--- +merge beneficiary data
    pdfAllPatBenef = pdfAllpat.merge(pdfBenef, on='BeneID', how='inner')

    #--- +merge provider data
    pdfAllPatBenefProv = pdfAllPatBenef.merge(pdfProvider, on='Provider', how='inner')
    
    #--- export data
    strPth_pklClaims = getPath_defPklClaims(blnIsTrain)
    print("TRACE (claims.loadCsv_claims):  pkl claim data file path ... ", strPth_pklClaims)
    pdfAllPatBenefProv.to_pickle(strPth_pklClaims)

    #print("INFO (csvClaims.shape):  ", pdfTest_allPatBenefProv.shape)
    return pdfAllPatBenefProv



def loadCsv_testClaims():
    #--- TODO:  make optional arg test or train data
    return loadCsv_claims(False)



def loadPkl_claims(blnIsTrain=False):
    strPth_pklClaims = getPath_defPklClaims(blnIsTrain)
    try:
        pdfClaims = pd.read_pickle(strPth_pklClaims)
    except FileNotFoundError:
        #--- catch:  there is no pickle file
        #--- load from csv instead;  will create pkl files for next time
        pdfClaims = loadCsv_claims(blnIsTrain)
    return pdfClaims



#--- feat eng
def do_featEng(pdfLoaded, blnIsTrain=False):
    print("INFO (claims.doFeatEng):  blnIsTrain, ", blnIsTrain)
    #--- remove cols
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
    pdfFeatEng['InscClaimReimbursement_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['InscClaimAmtReimbursed'].transform('mean') 
    pdfFeatEng['DeductibleAmtPaid_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['DeductibleAmtPaid'].transform('mean')
    
    pdfFeatEng['IPAnnualReimbursementAmt_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['IPAnnualReimbursementAmt'].transform('mean')
    pdfFeatEng['IPAnnualDeductibleAmt_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['IPAnnualDeductibleAmt'].transform('mean')

    pdfFeatEng['OPAnnualReimbursementAmt_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['OPAnnualReimbursementAmt'].transform('mean')
    pdfFeatEng['OPAnnualDeductibleAmt_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['OPAnnualDeductibleAmt'].transform('mean')
    return pdfFeatEng



#--- data eng on inpatient data
def prep_inpatData(pdfInpat):
    #--- calc admitted days
    pdfInpat['AdmissionDt'] = pd.to_datetime(pdfInpat['AdmissionDt'], format='%Y-%m-%d')
    pdfInpat['DischargeDt'] = pd.to_datetime(pdfInpat['DischargeDt'], format='%Y-%m-%d')
    pdfInpat['AdmittedDays'] = round((pdfInpat['DischargeDt'] - pdfInpat['AdmissionDt']).dt.days + 1)
    return pdfInpat



#--- data eng on beneficiary data
def prep_benefData(pdfBenef):
    #--- chronic condition cols;  change any vals of 2 to 0 
    aryCols = ['ChronicCond_Alzheimer', 'ChronicCond_Heartfailure', 
                'ChronicCond_KidneyDisease', 'ChronicCond_Cancer',
                'ChronicCond_ObstrPulmonary', 'ChronicCond_Depression',
                'ChronicCond_Diabetes', 'ChronicCond_IschemicHeart',
                'ChronicCond_Osteoporasis', 'ChronicCond_rheumatoidarthritis',
                'ChronicCond_stroke'] 

    for strVal in aryCols:
        pdfBenef.replace({strVal: 2}, 0, inplace=True)

    #--- fill missing data:  persons age
    kstrDatetime = '2019-12-01'                            #--- the est datetime for the dataset
    pdfBenef['DOB'] = pd.to_datetime(pdfBenef['DOB'], format = '%Y-%m-%d')
    pdfBenef['DOD'] = pd.to_datetime(pdfBenef['DOD'], format = '%Y-%m-%d') 
    pdfBenef['Age'] = round((pdfBenef['DOD'] - pdfBenef['DOB']).dt.days/365)
    pdfBenef['Age'].fillna(round(((pd.to_datetime(kstrDatetime, format='%Y-%m-%d') - pdfBenef['DOB']).dt.days)/365), inplace=True)

    #--- add an isDead flag column
    pdfBenef.loc[pdfBenef['DOD'].isna(), 'DeadOrNot'] = 0 
    pdfBenef.loc[pdfBenef['DOD'].notna(), 'DeadOrNot'] = 1 

    return pdfBenef



def get_logrPredict(pdfTestClaims):

    #--- logistic regression predictions;  load test data
    pdfClaims = pdfTestClaims
    #print("INFO (predict.pklClaims.shape):  ", pdfClaims.shape)

    pdfFeatEng = do_featEng(pdfClaims, False)
    npaScaled = mdl_utils.do_stdScaler(pdfFeatEng, False)
    pdfScaled = mdl_utils.do_stdScaler_toPdf(npaScaled)
    #print("INFO (predict.npaScaled.shape):  ", npaScaled.shape)

    ndaPredict = mdl_logR.predict(npaScaled)
    #print("INFO (predict.npaPredict.shape):  ", ndaPredict.shape)

    pdfPredict = pd.DataFrame(ndaPredict)
    #print("INFO (predict.pdfPredict.shape):  ", pdfPredict.shape)

    #--- stitch the grouped data with the labels
    pdfResults = pdfFeatEng.groupby(['Provider'], as_index=False).agg('sum')
    #print("INFO (predict.pdfGrpFeatEng.shape):  ", pdfResults.shape)

    pdfResults.insert(0, "hasAnom?", pdfPredict[0])
    return pdfResults    



def get_svmPredict(pdfTestClaims):

    #--- support vector machine predictions;  load test data
    pdfClaims = pdfTestClaims
    #print("INFO (predict.pklClaims.shape):  ", pdfClaims.shape)

    pdfFeatEng = do_featEng(pdfClaims, False)
    npaScaled = mdl_utils.do_stdScaler(pdfFeatEng, False)
    pdfScaled = mdl_utils.do_stdScaler_toPdf(npaScaled)
    #print("INFO (predict.npaScaled.shape):  ", npaScaled.shape)

    ndaPredict = mdl_svm.predict(npaScaled)
    #print("INFO (predict.npaPredict.shape):  ", ndaPredict.shape)

    pdfPredict = pd.DataFrame(ndaPredict)
    #print("INFO (predict.pdfPredict.shape):  ", pdfPredict.shape)

    #--- stitch the grouped data with the labels
    pdfResults = pdfFeatEng.groupby(['Provider'], as_index=False).agg('sum')
    #print("INFO (predict.pdfGrpFeatEng.shape):  ", pdfResults.shape)

    pdfResults.insert(0, "hasAnom?", pdfPredict[0])
    return pdfResults    



def get_xgbPredict(pdfTestClaims):

    #--- load test data
    pdfClaims = pdfTestClaims
    #print("INFO (predict.pklClaims.shape):  ", pdfClaims.shape)

    pdfFeatEng = do_featEng(pdfClaims, False)
    npaScaled = mdl_utils.do_stdScaler(pdfFeatEng, False)
    pdfScaled = mdl_utils.do_stdScaler_toPdf(npaScaled)
    #print("INFO (predict.npaScaled.shape):  ", npaScaled.shape)

    ndaPredict = mdl_xgb.predict(npaScaled)
    #print("INFO (predict.npaPredict.shape):  ", ndaPredict.shape)

    pdfPredict = pd.DataFrame(ndaPredict)
    #print("INFO (predict.pdfPredict.shape):  ", pdfPredict.shape)

    #--- stitch the grouped data with the labels
    pdfResults = pdfFeatEng.groupby(['Provider'], as_index=False).agg('sum')
    #print("INFO (predict.pdfGrpFeatEng.shape):  ", pdfResults.shape)

    pdfResults.insert(0, "hasAnom?", pdfPredict[0])
    return pdfResults



def get_encPredict(pdfTestClaims):

    #--- principal component analysis predictions;  load test data
    pdfClaims = pdfTestClaims
    #print("INFO (predict.pklClaims.shape):  ", pdfClaims.shape)

    pdfFeatEng = do_featEng(pdfClaims, False)                           #--- not grouped by provider
    

    #--- perform standard scaling; get fit then transform                      
    npaScaled = mdl_utils.do_stdScaler(pdfFeatEng, False)               #--- grouped by provider
    pdfScaled = mdl_utils.do_stdScaler_toPdf(npaScaled)
    #print("INFO (predict.npaScaled.shape):  ", npaScaled.shape)

    #--- perform PCA; then autoencode predict
    ndaPredict = mdl_autoenc.predict(pdfScaled)
    #print("INFO (predict.npaPredict.shape):  ", ndaPredict.shape)

    pdfPredict = pd.DataFrame(ndaPredict)
    #print("INFO (predict.pdfPredict.shape):  ", pdfPredict.shape)

    #--- stitch the grouped data with the labels
    pdfResults = pdfFeatEng.groupby(['Provider'], as_index=False).agg('sum')
    #print("INFO (predict.pdfGrpFeatEng.shape):  ", pdfResults.shape)

    pdfResults.insert(0, "hasAnom?", pdfPredict[0])
    return pdfResults    



def get_kmeansPredict(pdfTestClaims):

    pdfClaims = pdfTestClaims
    pdfFeatEng = do_featEng(pdfClaims, False)                           #--- not grouped by provider
    

    #--- perform standard scaling; get fit then transform                      
    npaScaled = mdl_utils.do_stdScaler(pdfFeatEng, False)               #--- grouped by provider
    pdfScaled = mdl_utils.do_stdScaler_toPdf(npaScaled)
    #print("INFO (predict.npaScaled.shape):  ", npaScaled.shape)

    #--- perform PCA; then autoencode predict
    ndaPredict = mdl_kmeans.predict(pdfScaled)
    #print("INFO (predict.npaPredict.shape):  ", ndaPredict.shape)

    pdfPredict = pd.DataFrame(ndaPredict)
    #print("INFO (predict.pdfPredict.shape):  ", pdfPredict.shape)

    #--- stitch the grouped data with the labels
    pdfResults = pdfFeatEng.groupby(['Provider'], as_index=False).agg('sum')
    #print("INFO (predict.pdfGrpFeatEng.shape):  ", pdfResults.shape)

    pdfResults.insert(0, "hasAnom?", pdfPredict[0])
    return pdfResults    