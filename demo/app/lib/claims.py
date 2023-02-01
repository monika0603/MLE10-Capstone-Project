import pandas as pd
import lib.utils as libPaths
#import os

#print("INFO:  ", os.getcwd())


#--- load, merge data from file
m_kstrDataPath = libPaths.pth_data
#def loadCsv_trainData():
def getPath_defPklClaims(blnIsTrain=False):
    global m_kstrDataPath
    strPrefix="test_"
    if (blnIsTrain):  strPrefix = "train_"
    strPth_pklClaims = m_kstrDataPath + strPrefix + 'claims.pkl'
    return strPth_pklClaims


#--- initialize paths
m_kstrPklClaims = m_kstrDataPath + 'deng_testClaims.pkl'
m_kstrPth_pklClaims = getPath_defPklClaims(blnIsTrain=False)



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


""" 
def loadPkl_testClaims():
    #--- convenience fxn to load the last processed claims data
    strPth_pklClaims = getPath_defPklClaims(False)
    #pdfClaims = pd.read_pickle(m_kstrPklClaims)
    pdfClaims = pd.read_pickle(strPth_pklClaims)
    #print("INFO (pklClaims.shape):  ", pdfClaims.shape)
    return pdfClaims """


def do_featEng(pdfLoaded):
    #--- remove cols
    #--- note:  remove the Potential Fraud column if it exists
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
    pdfFeatEng.loc[pdfFeatEng['RenalDiseaseIndicator'] == 'Y', 'RenalDiseaseIndicator'] = 1 
    pdfFeatEng['DeductibleAmtPaid'].fillna(0, inplace=True)
    pdfFeatEng['AdmittedDays'].fillna(0, inplace=True)

    #--- correlated cols

    #--- add new features to assist with predictions
    pdfFeatEng['InsClaimReimbursement_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['InscClaimAmtReimbursed'].transform('mean') 
    pdfFeatEng['DeductibleAmtPaid_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['DeductibleAmtPaid'].transform('mean')
    
    pdfFeatEng['IPAnnualReimbursementAmt_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['IPAnnualReimbursementAmt'].transform('mean')
    pdfFeatEng['IPAnnualDeductibleAmt_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['IPAnnualDeductibleAmt'].transform('mean')

    pdfFeatEng['OPAnnualReimbursementAmt_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['OPAnnualReimbursementAmt'].transform('mean')
    pdfFeatEng['OPAnnualDeductibleAmt_ProviderAvg'] = pdfFeatEng.groupby(['Provider'])['OPAnnualDeductibleAmt'].transform('mean')
    return pdfFeatEng



def do_stdScaler(pdfFeatEng):
    #--- Note:  prediction runs on X_val
    '''
    #--- WARN:  The default value of numeric_only in DataFrameGroupBy.sum is deprecated. 
    #           In a future version, numeric_only will default to False. Either specify 
    #           numeric_only or select only columns which should be valid for the function.
    '''

    #--- WARN:  this code groups all data by provider;  any predictions will also be by provider
    pdfGroupBy = pdfFeatEng.groupby(['Provider'], as_index=False).agg('sum')
    try:
        X = pdfGroupBy.drop(columns=['Provider', 'PotentialFraud'], axis=1)
    except KeyError:
        #--- catch:  there is no 'PotentialFraud' column
        X = pdfGroupBy.drop(columns=['Provider'], axis=1)

    #print("INFO:  ", X.columns)

    #--- apply scaler
    #--- WARN:  scaling is also grouped by provider
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()

    #--- note:  this is a numpy.ndarray
    X_std = scaler.transform(X)
    return X_std


def do_stdScaler_toPdf(npaScaled):
    #--- NOTE:  the list of cols came from do_stdScaler; print(X.columns)
    aryCols = ['InscClaimAmtReimbursed', 'DeductibleAmtPaid', 'AdmittedDays',
       'NoOfMonths_PartACov', 'NoOfMonths_PartBCov', 'ChronicCond_Alzheimer',
       'ChronicCond_Heartfailure', 'ChronicCond_KidneyDisease',
       'ChronicCond_Cancer', 'ChronicCond_ObstrPulmonary',
       'ChronicCond_Depression', 'ChronicCond_Diabetes',
       'ChronicCond_IschemicHeart', 'ChronicCond_Osteoporasis',
       'ChronicCond_rheumatoidarthritis', 'ChronicCond_stroke',
       'IPAnnualReimbursementAmt', 'IPAnnualDeductibleAmt',
       'OPAnnualReimbursementAmt', 'OPAnnualDeductibleAmt', 'Age', 'DeadOrNot',
       'Gender_2', 'Race_2', 'Race_3', 'Race_5',
       'ClaimReimbursement_ProviderAvg',
       'ClaimReimbursement_AttendingPhysician',
       'ClaimReimbursement_OperatingPhysician',
       'DeductibleAmtPaid_ProviderAvg', 'DeductibleAmtPaid_AttendingPhysician',
       'DeductibleAmtPaid_OperatingPhysician']

    #npaScaled = do_stdScaler(pdfFeatEng)
    pdfScaled = pd.DataFrame(npaScaled, columns=aryCols)
    return pdfScaled


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